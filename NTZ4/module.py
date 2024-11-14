import random
# a. Умножение «матрица - матрица»
def matrix_multiply(A, B):
    result = [[sum(x * y for x, y in zip(row, col)) for col in zip(*B)] for row in A]
    return result

# b. Умножение «матрица - вектор»
def matrix_vector_multiply(matrix, vector):
    result = [sum(row[i] * vector[i] for i in range(len(vector))) for row in matrix]
    return result

# c. Расчет следа матрицы (сумма диагональных элементов)
def trace(matrix):
    return sum(matrix[i][i] for i in range(len(matrix)))

# d. Скалярное произведение двух векторов
def dot_product(vector1, vector2):
    return sum(x * y for x, y in zip(vector1, vector2))

# e. Расчет гистограммы для вектора с изменяемым количеством квантов
def histogram(vector, bins):
    min_val, max_val = min(vector), max(vector)
    bin_size = (max_val - min_val) / bins
    histogram = [0] * bins
    for value in vector:
        index = min(int((value - min_val) / bin_size), bins - 1)
        histogram[index] += 1
    return histogram

# f. Фильтрация вектора ядерным фильтром (например, [-1, 0, 1])
def apply_kernel_filter(vector, kernel):
    k_size = len(kernel)
    pad = k_size // 2
    result = []
    for i in range(pad, len(vector) - pad):
        result.append(sum(vector[i + j - pad] * kernel[j] for j in range(k_size)))
    return result

# g. Чтение/запись данных в файл
def write_to_file(filename, data):
    with open(filename, 'w') as file:
        file.write(data)

def read_from_file(filename):
    with open(filename, 'r') as file:
        return file.read()