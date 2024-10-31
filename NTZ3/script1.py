def print_table(operation):
    for i in range(1, 10):
        for j in range(1, 10):
            if operation == 'умножение':
                result = i * j
                print(f"{i} * {j} = {result}", end="\t")
            elif operation == 'деление':
                result = i / j
                print(f"{i} / {j:.2f}", end="\t")
            elif operation == 'вычитание':
                result = i - j
                print(f"{i} - {j} = {result}", end="\t")
            elif operation == 'сложение':
                result = i + j
                print(f"{i} + {j} = {result}", end="\t")
        print()

operation = input("Введите тип таблицы (умножение, деление, вычитание, сложение): ")
print_table(operation)
