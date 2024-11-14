import time
import random
import numpy as np
from module import (
    matrix_multiply,
    matrix_vector_multiply,
    trace,
    dot_product,
    histogram,
    apply_kernel_filter,
    write_to_file
)

#def time_execution(func, *args):
#    start_time = time.time()
#    func(*args)
#    return (time.time() - start_time) * 1000

def time_execution(func, *args, repeats=100):
    total_time = 0
    for _ in range(repeats):
        start_time = time.time()
        func(*args)
        total_time += (time.time() - start_time)
    return (total_time / repeats) * 1000

def generate_random_vector(size):
    return [random.random() for _ in range(size)]

def generate_random_matrix(rows, cols):
    return [[random.random() for _ in range(cols)] for _ in range(rows)]

def generate_np_matrix_vector(size):
    return np.random.rand(size, size), np.random.rand(size)

def measure_and_save_times(filename, optimized):
    size = 20
    results = ""

    if optimized:
        A, B = np.random.rand(size, size), np.random.rand(size, size)
        matrix_duration = time_execution(np.dot, A, B)
        results += f"optimized_matrix_multiply ({size}x{size}): {matrix_duration} seconds\n"

        matrix, vector = generate_np_matrix_vector(size)
        matrix_vector_duration = time_execution(np.dot, matrix, vector)
        results += f"optimized_matrix_vector_multiply ({size}x{size}): {matrix_vector_duration} seconds\n"

        trace_duration = time_execution(np.trace, matrix)
        results += f"optimized_trace ({size}x{size}): {trace_duration} seconds\n"

        vector1, vector2 = np.random.rand(size), np.random.rand(size)
        dot_duration = time_execution(np.dot, vector1, vector2)
        results += f"optimized_dot_product (size {size}): {dot_duration} seconds\n"

    else:
        A, B = generate_random_matrix(size, size), generate_random_matrix(size, size)
        matrix_duration = time_execution(matrix_multiply, A, B)
        results += f"matrix_multiply ({size}x{size}): {matrix_duration} seconds\n"

        matrix, vector = generate_random_matrix(size, size), generate_random_vector(size)
        matrix_vector_duration = time_execution(matrix_vector_multiply, matrix, vector)
        results += f"matrix_vector_multiply ({size}x{size}): {matrix_vector_duration} seconds\n"

        trace_duration = time_execution(trace, matrix)
        results += f"trace ({size}x{size}): {trace_duration} seconds\n"

        vector1, vector2 = generate_random_vector(size), generate_random_vector(size)
        dot_duration = time_execution(dot_product, vector1, vector2)
        results += f"dot_product (size {size}): {dot_duration} seconds\n"

        histogram_duration = time_execution(histogram, vector, 10)
        results += f"histogram (size {size}): {histogram_duration} seconds\n"

        kernel = [-1, 0, 1]
        filter_duration = time_execution(apply_kernel_filter, vector, kernel)
        results += f"apply_kernel_filter (size {size}): {filter_duration} seconds\n"

    write_to_file(filename, results)

measure_and_save_times("time_measurements.txt", optimized=False)
measure_and_save_times("optimized_time_measurements.txt", optimized=True)
