import random

# a. Создание вектора
def create_vector(N):
    return [random.random() for _ in range(N)]

# b. Создание матрицы
def create_matrix(M, N):
    return [[random.random() for _ in range(N)] for _ in range(M)]

# c. Умножение матрицы на вектор
def multiply_matrix_vector(matrix, vector):
    result = [sum(row[i] * vector[i] for i in range(len(vector))) for row in matrix]
    return result

# d. Печать матрицы
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(f"{val:.2f}" for val in row))

# e. Печать вектора
def print_vector(vector):
    print(" ".join(f"{val:.2f}" for val in vector))

# f. Сумма диагональных элементов матрицы
def sum_diagonal(matrix):
    return sum(matrix[i][i] for i in range(min(len(matrix), len(matrix[0]))))

# g. Двумерная свертка изображения
def convolve_2d(matrix, kernel):
    kernel_size = len(kernel)
    pad = kernel_size // 2
    result = []

    for i in range(pad, len(matrix) - pad):
        row = []
        for j in range(pad, len(matrix[0]) - pad):
            cell_value = sum(matrix[i + ki - pad][j + kj - pad] * kernel[ki][kj]
                             for ki in range(kernel_size) for kj in range(kernel_size))
            row.append(cell_value)
        result.append(row)
    return result

# Пример использования
vector = create_vector(5)
matrix = create_matrix(3, 5)
print("Вектор:")
print_vector(vector)
print("\nМатрица:")
print_matrix(matrix)
print("\nРезультат умножения матрицы на вектор:")
print_vector(multiply_matrix_vector(matrix, vector))
print("\nСумма диагональных элементов матрицы:")
print(sum_diagonal(matrix))
