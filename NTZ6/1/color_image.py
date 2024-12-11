from base_image import ImageBase
import numpy as np

class ColorImage(ImageBase):
    def __init__(self, data):
        data = np.clip(np.array(data), 0, 255)
        assert data.ndim == 3 and data.shape[2] == 3, "Color images must have 3 channels (RGB)."
        super().__init__(data)