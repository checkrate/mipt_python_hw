# Задание 1
while True:
    try:
        user_input1 = input("Введите первое число (или b для выхода): ")
        if user_input1.lower() == 'b':
            print("Выход из программы...")
            break
        num1 = float(user_input1)
        
        user_input2 = input("Введите второе число (или b для выхода): ")
        if user_input2.lower() == 'b':
            print("Выход из программы...")
            break
        num2 = float(user_input2)
        
        print("Сумма:", num1 + num2)
    except ValueError:
        print("Пожалуйста, вводите только числа.")

# Задание 2
pattern = [
    ["*", "1", "*", "2", "*"],
    ["3", "*", "4", "*", "5"],
    ["*", "6", "*", "7", "*"],
    ["8", "*", "9", "*", "10"],
    ["*", "11", "*", "12", "*"]
]

for row in pattern:
    print(" ".join(row))

# Задание 3
print("Загадайте число и укажите интервал.")
min_num = int(input("Введите минимальное значение интервала: "))
max_num = int(input("Введите максимальное значение интервала: "))
    
while True:
    guess = (min_num + max_num) // 2
    print(f"Число равно {guess}?")
    response = input("Введите <, > или y (или b для выхода):")
        
    if response == "y":
        print("Программа угадала ваше число!")
        break
    elif response == "<":
        max_num = guess - 1
    elif response == ">":
        min_num = guess + 1
    elif response == 'b':
        print("Выход из программы...")
        break
    else:
        print("Некорректный ввод. Попробуйте снова.")


# Задание 4
numbers = list(map(int, input("Введите список чисел, разделенных пробелами (0 для завершения): ").split()))

max_num = 0
for num in numbers:
    if num == 0:
        break
    if num > max_num:
        max_num = num

print("Наибольшее число:", max_num)


# Задание 5
for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i} x {j} = {i * j}")
    print()

# Задание 6
values = [3, 1, 4, 1, 5, 9, 2, 6, 5, 3, 5]

min_val = min(values)
max_val = max(values)

sorted_values = sorted(values)
n = len(sorted_values)

if n % 2 == 1:
    median_val = sorted_values[n // 2]
else:
    median_val = (sorted_values[n // 2 - 1] + sorted_values[n // 2]) / 2

print('Список:', values)
print("Минимум:", min_val)
print("Максимум:", max_val)
print("Медиана:", median_val)


# Задание 7
import random

values = [random.randint(0, 100) for _ in range(20)]
histogram = [0] * 10
for value in values:
    histogram[value // 10] += 1

probabilities = [count / len(values) for count in histogram]

print("Гистограмма:", histogram)
print("Вероятности:", probabilities)

# Задание 8
import random

N = int(input("Введите размерность векторов: "))
vector1 = [random.randint(0, 100) for _ in range(N)]
vector2 = [random.randint(0, 100) for _ in range(N)]

sum_vector = [x + y for x, y in zip(vector1, vector2)]
prod_vector = [x * y for x, y in zip(vector1, vector2)]

norm1 = sum(x**2 for x in vector1) ** 0.5
norm2 = sum(x**2 for x in vector2) ** 0.5

larger_norm_vector = vector1 if norm1 > norm2 else vector2
scalar = float(input("Введите скаляр: "))
scaled_vector = [x * scalar for x in larger_norm_vector]

print("Сумма:", sum_vector)
print("Умножение:", prod_vector)
print("Вектор с большей нормой:", larger_norm_vector)
print("Результат умножения на скаляр:", scaled_vector)

# Задание 9
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9]
]
vector = [1, 2, 3]

result = [sum(m * v for m, v in zip(row, vector)) for row in matrix]
print("Результат умножения матрицы на вектор:", result)

# Задание 10
values = [5, -3, 6, -1, -2, 7, -6, 4]
for i in range(1, len(values) - 1):
    if values[i] < 0:
        left = next(x for x in reversed(values[:i]) if x > 0)
        right = next(x for x in values[i+1:] if x > 0)
        values[i] = (left + right) / 2

print("Модифицированный список:", values)

# Задание 11
data = [1, 2, 3, 4, 5, 6, 7, 8, 9]
kernel = [1, 0, -1]
convolution = [
    sum(data[i + k] * kernel[k] for k in range(len(kernel)))
    for i in range(len(data) - len(kernel) + 1)
]

print("Результат свертки:", convolution)

