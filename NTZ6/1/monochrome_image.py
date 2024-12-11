from base_image import ImageBase
import numpy as np

class MonochromeImage(ImageBase):
    def __init__(self, data):
        data = np.clip(np.array(data), 0, 255)
        super().__init__(data)