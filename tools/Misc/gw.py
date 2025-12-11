import time
import asyncio
from concurrent.futures import ThreadPoolExecutor, ProcessPoolExecutor
import os

# ----------------------------
# CPU-bound task
# ----------------------------
def cpu_task(n: int):
    total = 0
    for i in range(n):
        total += i * i
    return total

# ----------------------------
# IO-bound async task
# ----------------------------
async def async_task(duration: float):
    await asyncio.sleep(duration)
    return duration

# ----------------------------
# IO-bound function for threads/processes
# ----------------------------
def io_task(duration: float):
    time.sleep(duration)
    return duration

# ----------------------------
# Benchmark helpers
# ----------------------------
def benchmark_threads(task_func, n_tasks, *args, max_workers=None):
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(task_func, *args) for _ in range(n_tasks)]
        for f in futures:
            f.result()
    return time.perf_counter() - start

def benchmark_processes(task_func, n_tasks, *args, max_workers=None):
    start = time.perf_counter()
    with ProcessPoolExecutor(max_workers=max_workers) as ex:
        futures = [ex.submit(task_func, *args) for _ in range(n_tasks)]
        for f in futures:
            f.result()
    return time.perf_counter() - start

async def benchmark_async(task_func, n_tasks, *args):
    start = time.perf_counter()
    tasks = [asyncio.create_task(task_func(*args)) for _ in range(n_tasks)]
    await asyncio.gather(*tasks)
    return time.perf_counter() - start

# ----------------------------
# Main benchmarking
# ----------------------------
def run_benchmarks():
    cpu_iterations = 5_000_000   # CPU-heavy
    io_duration = 0.2            # seconds per I/O task
    n_tasks_list = [1, 2, 4, 8, 16, 32]

    print(f"CPU cores detected: {os.cpu_count()}\n")

    print("=== CPU-bound task ===")
    print(f"{'Tasks':>8}  {'Threads(s)':>12}  {'Processes(s)':>12}")
    print("-" * 38)
    for n in n_tasks_list:
        t_threads = benchmark_threads(cpu_task, n, cpu_iterations)
        t_processes = benchmark_processes(cpu_task, n, cpu_iterations)
        print(f"{n:>8}  {t_threads:>12.4f}  {t_processes:>12.4f}")

    print("\n=== IO-bound task ===")
    print(f"{'Tasks':>8}  {'Threads(s)':>12}  {'Async(s)':>12}  {'Processes(s)':>12}")
    print("-" * 56)
    for n in n_tasks_list:
        t_threads = benchmark_threads(io_task, n, io_duration)
        t_processes = benchmark_processes(io_task, n, io_duration)
        t_async = asyncio.run(benchmark_async(async_task, n, io_duration))
        print(f"{n:>8}  {t_threads:>12.4f}  {t_async:>12.4f}  {t_processes:>12.4f}")

if __name__ == "__main__":
    run_benchmarks()