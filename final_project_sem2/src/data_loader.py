import os
import cv2
import numpy as np
from glob import glob
from sklearn.model_selection import train_test_split

import albumentations as A
from albumentations.pytorch import ToTensorV2

import config
import torch


def load_image_paths(img_dir, mask_dir=None):
    imgs = sorted(glob(os.path.join(img_dir, '*.*')))
    if mask_dir:
        masks = sorted(glob(os.path.join(mask_dir, '*.*')))
        return list(zip(imgs, masks))
    return imgs


def get_train_val_split(test_size=0.2, random_state=42):
    pairs = load_image_paths(config.TRAIN_IMG_DIR, config.TRAIN_MASK_DIR)
    train, val = train_test_split(pairs, test_size=test_size, random_state=random_state)
    return train, val


class CellDataset(torch.utils.data.Dataset):
    """PyTorch Dataset for images and masks"""
    def __init__(self, pairs, augment=False):
        self.pairs = pairs
        self.augment = augment
        self.aug = A.Compose([
            A.HorizontalFlip(),
            A.VerticalFlip(),
            A.Rotate(max_angle=90),
        ]) if augment else None

    def __len__(self):
        return len(self.pairs)

    def __getitem__(self, idx):
        img_path, mask_path = self.pairs[idx]
        img = cv2.imread(img_path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        mask = (mask > 0).astype('float32')[..., None]

        if self.augment:
            aug = self.aug(image=img, mask=mask)
            img, mask = aug['image'], aug['mask']

        img = img.astype('float32') / 255.0
        img = np.transpose(img, (2, 0, 1))
        mask = np.transpose(mask, (2, 0, 1))

        return torch.tensor(img), torch.tensor(mask)