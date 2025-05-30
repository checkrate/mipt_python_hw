import numpy as np
from skimage.feature import greycomatrix, greycoprops, local_binary_pattern
from sklearn.ensemble import RandomForestRegressor

class PatchRegressor:
    def __init__(self, patch_size=64, stride=32, rf_params=None):
        self.patch_size = patch_size
        self.stride = stride
        self.model = RandomForestRegressor(**(rf_params or {}))

    def _extract_features(self, patch):
        glcm = greycomatrix(patch, [1], [0], 256, symmetric=True, normed=True)
        contrast = greycoprops(glcm, 'contrast')[0,0]
        dissimilarity = greycoprops(glcm, 'dissimilarity')[0,0]
        homogeneity = greycoprops(glcm, 'homogeneity')[0,0]
        energy = greycoprops(glcm, 'energy')[0,0]
        correlation = greycoprops(glcm, 'correlation')[0,0]
        lbp = local_binary_pattern(patch, P=8, R=1.0)
        lbp_hist, _ = np.histogram(lbp.ravel(), bins=16, range=(0,16))
        lbp_hist = lbp_hist.astype('float32') / lbp_hist.sum()
        return np.hstack([contrast, dissimilarity, homogeneity,
                          energy, correlation, lbp_hist])

    def _make_patches(self, img):
        h, w = img.shape
        for y in range(0, h - self.patch_size + 1, self.stride):
            for x in range(0, w - self.patch_size + 1, self.stride):
                patch = img[y:y+self.patch_size, x:x+self.patch_size]
                yield (x, y, patch)

    def fit(self, images, counts):
        X, y = [], []
        for img, cnt in zip(images, counts):
            gray = img if img.ndim==2 else img.mean(axis=2).astype('uint8')
            npatches = 0
            for _, _, p in self._make_patches(gray):
                feats = self._extract_features(p)
                X.append(feats)
                y.append(cnt / ((gray.shape[0]//self.patch_size) * (gray.shape[1]//self.patch_size)))
                npatches += 1
        self.model.fit(np.array(X), np.array(y))

    def predict_full_image(self, img):
        gray = img if img.ndim==2 else img.mean(axis=2).astype('uint8')
        total = 0
        for _, _, p in self._make_patches(gray):
            feats = self._extract_features(p)
            total += self.model.predict([feats])[0]
        return int(round(total))