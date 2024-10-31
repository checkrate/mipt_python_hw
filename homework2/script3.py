def channel_filter_decorator(filter_function):
    def wrapper(image):
        channels = len(image[0][0])
        return [
            [
                [filter_function([[image[i][j][c] for j in range(len(image[0]))]
                                  for i in range(len(image))])
                 for c in range(channels)]
            ]
        ]
    return wrapper

def sample_filter(channel):
    # Пример фильтрации — просто возвращаем сам канал для примера
    return channel

multi_channel_filter = channel_filter_decorator(sample_filter)
