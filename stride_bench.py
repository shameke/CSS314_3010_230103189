import numpy as np
import time
import statistics
import csv
import os
import time, numpy as np

data = np.ones(16_777_216, dtype=np.float64)
strides = [1, 2, 4, 8, 16, 32, 64, 128]

results = []

for stride in strides:
    times = []

    # Warm-up: 5 runs
    for _ in range(5):
        total = 0.0
        for i in range(0, len(data), stride):
            total += data[i]

    # Measurement: 5 runs
    for _ in range(5):
        total = 0.0
        start = time.perf_counter_ns()

        for i in range(0, len(data), stride):
            total += data[i]

        end = time.perf_counter_ns()
        times.append(end - start)

    median_time = statistics.median(times)
    elements_touched = len(range(0, len(data), stride))
    latency = median_time / elements_touched

    results.append([
        stride,
        median_time,
        elements_touched,
        latency
    ])
    os.makedirs("results", exist_ok=True)

    with open("results/stride_results.tsv", "w", newline="") as file:
        writer = csv.writer(file, delimiter="\t")

        writer.writerow([
            "Stride",
            "Median_Time_ns",
            "Elements_Touched",
            "Latency_ns_per_element"
        ])

        writer.writerows(results)

    print("Results saved to results/stride_results.tsv")
