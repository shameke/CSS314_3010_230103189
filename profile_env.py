from salt import get_student_params
import platform
import json
import os
import psutil
import sys


def get_cpu_info():
    cpu = platform.processor()

    return {
        "cpu_model": cpu,
        "physical_cores": psutil.cpu_count(logical=False),
        "logical_cores": psutil.cpu_count(logical=True),
        "architecture": platform.machine(),
        "frequency_mhz": psutil.cpu_freq().current if psutil.cpu_freq() else None
    }


def get_memory_info():
    return {
        "ram_total_gb": round(psutil.virtual_memory().total / (1024 ** 3), 2)
    }


def main():
    os.makedirs("results", exist_ok=True)

    profile = {
        "cpu": get_cpu_info(),
        "memory": get_memory_info(),
        "operating_system": platform.platform(),
        "python_version": sys.version,
        "python_implementation": platform.python_implementation()
    }

    student_params = get_student_params("230103189")

    with open("results/salted_params.json", "w") as file:
        json.dump(student_params, file, indent=4)

    print(json.dumps(profile, indent=4))
    print("\nHost profile saved successfully!")


if __name__ == "__main__":
    main()