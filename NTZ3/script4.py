def rgb_to_yiq(rgb):
    r, g, b = rgb
    y = 0.299 * r + 0.587 * g + 0.114 * b
    i = 0.596 * r - 0.275 * g - 0.321 * b
    q = 0.212 * r - 0.523 * g + 0.311 * b
    return [y, i, q, 1]

def yiq_to_rgb(yiq):
    y, i, q = yiq
    r = y + 0.956 * i + 0.621 * q
    g = y - 0.272 * i - 0.647 * q
    b = y - 1.106 * i + 1.703 * q
    return [r, g, b, 0] 

def convert_color(color_vector):
    if color_vector[3] == 0:
        return rgb_to_yiq(color_vector[:3])
    elif color_vector[3] == 1:
        return yiq_to_rgb(color_vector[:3])

# Пример использования
color_rgb = [0.5, 0.2, 0.7, 0]  # RGB
color_yiq = convert_color(color_rgb)
print("Преобразование RGB в YIQ:", color_yiq)

color_converted_back = convert_color(color_yiq)
print("Преобразование обратно в RGB:", color_converted_back)
