from base_image import ImageBase
import numpy as np

class BinaryImage(ImageBase):
    def __init__(self, data):
        data = np.where(np.array(data) > 0, 1, 0)
        super().__init__(data)