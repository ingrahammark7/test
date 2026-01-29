import os
import time
import random

# --- True hardware RNG on Android ---
def true_random_float():
    try:
        with open("/dev/urandom", "rb") as f:
            # Read 4 bytes and convert to float between 0 and 1
            val = int.from_bytes(f.read(4), "big") / 0xFFFFFFFF
            return val
    except Exception:
        return 0.0  # fallback if /dev/urandom fails

# --- CPU usage from /proc/stat ---
def get_cpu_percent(prev_total=0, prev_idle=0):
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        parts = line.split()
        if parts[0] != "cpu":
            return 0.0, 0, 0

        values = list(map(int, parts[1:]))
        idle = values[3] + values[4]  # idle + iowait
        total = sum(values)

        diff_total = total - prev_total if prev_total else 0
        diff_idle = idle - prev_idle if prev_idle else 0
        cpu_percent = (1.0 - diff_idle/diff_total) if diff_total else 0.0

        return cpu_percent, total, idle
    except Exception:
        return 0.0, 0, 0

# --- Memory usage ---
def read_mem_usage():
    try:
        with open("/proc/meminfo") as f:
            meminfo = f.readlines()
        mem_total = int(meminfo[0].split()[1]) / 1024  # KB to MB
        mem_free = int(meminfo[1].split()[1]) / 1024
        mem_available = int(meminfo[2].split()[1]) / 1024
        return mem_total, mem_free, mem_available
    except Exception:
        return 0, 0, 0

# --- Python memory usage ---
def top_python_process():
    try:
        pid = os.getpid()
        with open(f"/proc/{pid}/status") as f:
            for line in f:
                if line.startswith("VmRSS:"):
                    return int(line.split()[1]) / 1024  # KB to MB
        return 0
    except Exception:
        return 0

# --- Metrics collector ---
class MetricsCollector:
    def __init__(self, window_size=5):
        self.window_size = window_size
        self.cpu_window = []

    def collect(self):
        # CPU
        prev_total, prev_idle = self.cpu_window[-1] if self.cpu_window else (0, 0)
        cpu_percent, total, idle = get_cpu_percent(prev_total, prev_idle)
        self.cpu_window.append((total, idle))
        if len(self.cpu_window) > self.window_size:
            self.cpu_window.pop(0)

        # Memory
        mem_total, mem_free, mem_available = read_mem_usage()
        py_mem = top_python_process()
        rng_val = true_random_float()

        return {
            "cpu": cpu_percent,
            "mem_total": mem_total,
            "mem_free": mem_free,
            "mem_available": mem_available,
            "py_mem": py_mem,
            "rng": rng_val
        }

def main(iterations=20, interval=1.0):
    collector = MetricsCollector(window_size=5)
    for i in range(iterations):
        metrics = collector.collect()
        print(f"[Iteration {i+1}/{iterations}] "
              f"CPU={metrics['cpu']*100:.2f}%, "
              f"Mem={metrics['mem_total']:.2f}/{metrics['mem_free']:.2f}/{metrics['mem_available']:.2f} MB, "
              f"Python Mem={metrics['py_mem']:.2f} MB, "
              f"RNG={metrics['rng']:.6f}")
        time.sleep(interval)

if __name__ == "__main__":
    main()