from binary_image import BinaryImage
from monochrome_image import MonochromeImage
from color_image import ColorImage
from image_converter import ImageConverter

# Пример данных
binary_data = [[0, 1, 0], [1, 0, 1], [0, 1, 0]]
mono_data = [[100, 150, 200], [50, 75, 125], [25, 50, 75]]
color_data = [[[255, 0, 0], [0, 255, 0], [0, 0, 255]], [[128, 128, 0], [0, 128, 128], [128, 0, 128]]]

binary_image = BinaryImage(binary_data)
mono_image = MonochromeImage(mono_data)
color_image = ColorImage(color_data)

converter = ImageConverter()
corrected_mono = converter.monochrome_to_monochrome(mono_image)
gray_from_color = converter.color_to_monochrome(color_image)

print(corrected_mono.get_data())
print(gray_from_color.get_data())
