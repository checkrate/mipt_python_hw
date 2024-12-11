import numpy as np

class ImageBase:
    def __init__(self, data):
        self.data = np.array(data)

    def get_data(self):
        return self.data