import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

import config
from data_loader import get_train_val_split, CellDataset

class DoubleConv(nn.Module):
    def __init__(self, in_ch, out_ch):
        super().__init__()
        self.net = nn.Sequential(
            nn.Conv2d(in_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_ch, out_ch, 3, padding=1),
            nn.BatchNorm2d(out_ch),
            nn.ReLU(inplace=True),
        )
    def forward(self, x): return self.net(x)

class UNet(nn.Module):
    def __init__(self, in_ch, out_ch, features):
        super().__init__()
        self.downs = nn.ModuleList()
        self.ups = nn.ModuleList()
        for feature in features:
            self.downs.append(DoubleConv(in_ch, feature))
            in_ch = feature
        for feature in reversed(features):
            self.ups.append(nn.ConvTranspose2d(feature*2, feature, 2, stride=2))
            self.ups.append(DoubleConv(feature*2, feature))
        self.bottleneck = DoubleConv(features[-1], features[-1]*2)
        self.final = nn.Conv2d(features[0], out_ch, 1)

    def forward(self, x):
        skips = []
        for down in self.downs:
            x = down(x)
            skips.append(x)
            x = nn.MaxPool2d(2)(x)
        x = self.bottleneck(x)
        skips = skips[::-1]
        for idx in range(0, len(self.ups), 2):
            x = self.ups[idx](x)
            skip = skips[idx//2]
            x = torch.cat((skip, x), dim=1)
            x = self.ups[idx+1](x)
        return torch.sigmoid(self.final(x))

class UNetTrainer:
    def __init__(self, cfg=config.DL):
        self.cfg = cfg
        self.device = cfg['device']
        self.model = UNet(cfg['in_channels'], cfg['out_channels'], cfg['features']).to(self.device)
        self.optimizer = optim.Adam(self.model.parameters(), lr=cfg['lr'])
        self.criterion = nn.BCELoss()

    def train(self):
        train_pairs, val_pairs = get_train_val_split()
        train_loader = DataLoader(CellDataset(train_pairs, augment=True),
                                  batch_size=self.cfg['batch_size'], shuffle=True)
        for epoch in range(self.cfg['epochs']):
            self.model.train()
            total_loss = 0
            for imgs, masks in train_loader:
                imgs, masks = imgs.to(self.device), masks.to(self.device)
                preds = self.model(imgs)
                loss = self.criterion(preds, masks)
                self.optimizer.zero_grad()
                loss.backward()
                self.optimizer.step()
                total_loss += loss.item()
            print(f"Epoch {epoch+1}/{self.cfg['epochs']} - Loss: {total_loss/len(train_loader):.4f}")

    def predict(self, img):
        self.model.eval()
        x = torch.tensor(img.astype('float32')/255.0).permute(2,0,1).unsqueeze(0).to(self.device)
        with torch.no_grad():
            mask = self.model(x)
        return (mask.squeeze().cpu().numpy() > 0.5).astype('uint8')

    def count_from_mask(self, mask):
        import cv2
        cnts, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return len(cnts)