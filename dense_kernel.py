
import numpy as np
import time
import statistics
import json
import os

# Load individual matrix size
with open("results/salted_params.json", "r") as file:
    params = json.load(file)

N = params["N"]
M = N // 2

print("Matrix size:", N)
print("Working size:", M)

# Create matrices
A = np.random.rand(N, N)
B = np.random.rand(N, N)


def multiply_naive(A, B, M):
    C = np.zeros((M, M))

    for i in range(M):
        for j in range(M):
            total = 0
            for k in range(M):
                total += A[i, k] * B[k, j]
            C[i, j] = total

    return C


def multiply_interchanged(A, B, M):
    C = np.zeros((M, M))

    for i in range(M):
        for k in range(M):
            temp = A[i, k]
            for j in range(M):
                C[i, j] += temp * B[k, j]

    return C


def benchmark(function, A, B, M):
    times = []

    for _ in range(3):
        start = time.perf_counter()
        result = function(A, B, M)
        end = time.perf_counter()

        times.append(end - start)

    return statistics.median(times)


# Run naive benchmark
print("Starting naive benchmark...")
naive_time = benchmark(multiply_naive, A, B, M)
print("Naive benchmark finished")

# Run interchanged benchmark
print("Starting interchanged benchmark...")
interchanged_time = benchmark(multiply_interchanged, A, B, M)
print("Interchanged benchmark finished")

# Calculate speedup
speedup = naive_time / interchanged_time

print("Naive time:", naive_time)
print("Interchanged time:", interchanged_time)
print("Speedup:", speedup)

# Check results
print("Checking results...")
C1 = multiply_naive(A, B, M)
C2 = multiply_interchanged(A, B, M)

results_equal = np.allclose(C1, C2)
print("Results are equal:", results_equal)

# Save results
os.makedirs("results", exist_ok=True)

output = {
    "matrix_size": N,
    "working_size": M,
    "naive_time_seconds": naive_time,
    "interchanged_time_seconds": interchanged_time,
    "speedup": speedup,
    "results_equal": bool(results_equal)
}

with open("results/loop_interchange.json", "w") as file:
    json.dump(output, file, indent=4)

print("Results saved to results/loop_interchange.json")
