import time

def measure_additions_per_second(duration_seconds=5):
    count = 0
    start_time = time.time()
    x = 0
    while time.time() - start_time < duration_seconds:
        x += 1
        count += 1
    elapsed = time.time() - start_time
    ops_per_second = count / elapsed
    print(f"Performed {count} additions in {elapsed:.4f} seconds.")
    print(f"Approximate additions per second: {ops_per_second:.2e}")

if __name__ == "__main__":
    measure_additions_per_second()