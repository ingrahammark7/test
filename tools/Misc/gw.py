import psutil
import time
import random
import sys

# -------------------------------
# RNG setup
# -------------------------------
def real_rng():
    """Use Python's real random."""
    return random.random()

# -------------------------------
# Metrics collection
# -------------------------------
def get_cpu_usage():
    """
    Returns total CPU usage % averaged over 0.5 seconds.
    """
    try:
        return psutil.cpu_percent(interval=0.5)
    except Exception as e:
        print(f"[CPU Error] {e}")
        return 0.0

def get_memory_usage():
    """
    Returns memory usage in MB (used, total)
    """
    try:
        mem = psutil.virtual_memory()
        used_mb = (mem.total - mem.available) / (1024 * 1024)
        total_mb = mem.total / (1024 * 1024)
        return round(used_mb, 2), round(total_mb, 2)
    except Exception as e:
        print(f"[Memory Error] {e}")
        return 0.0, 0.0

def get_process_count():
    """
    Returns number of running processes
    """
    try:
        return len(psutil.pids())
    except Exception as e:
        print(f"[Process Error] {e}")
        return 0

# -------------------------------
# Metrics Window Handling
# -------------------------------
class MetricsWindow:
    def __init__(self, size=5):
        self.size = size
        self.data = []

    def add(self, cpu, mem, proc):
        self.data.append({'cpu': cpu, 'mem': mem, 'proc': proc})
        if len(self.data) > self.size:
            self.data.pop(0)

    def summary(self):
        if not self.data:
            return {"cpu":0, "mem":0, "proc":0, "cpu_min":0, "cpu_max":0,
                    "mem_min":0, "mem_max":0, "proc_min":0, "proc_max":0}
        cpu_vals = [d['cpu'] for d in self.data]
        mem_vals = [d['mem'] for d in self.data]
        proc_vals = [d['proc'] for d in self.data]
        return {
            "cpu": round(sum(cpu_vals)/len(cpu_vals), 2),
            "mem": round(sum(mem_vals)/len(mem_vals), 2),
            "proc": round(sum(proc_vals)/len(proc_vals), 2),
            "cpu_min": min(cpu_vals),
            "cpu_max": max(cpu_vals),
            "mem_min": min(mem_vals),
            "mem_max": max(mem_vals),
            "proc_min": min(proc_vals),
            "proc_max": max(proc_vals)
        }

# -------------------------------
# Main Loop
# -------------------------------
def main_loop(window_size=5, iterations=20, sleep_sec=1):
    window = MetricsWindow(size=window_size)
    for i in range(iterations):
        cpu = get_cpu_usage()
        mem_used, mem_total = get_memory_usage()
        proc_count = get_process_count()

        window.add(cpu, mem_used, proc_count)
        summary = window.summary()

        # Mock prediction metric (replace with your model)
        prediction_confidence = real_rng()  # Use real RNG
        accuracy = round(prediction_confidence * 100, 2)

        print(f"[Window {i+1}/{iterations}, Size={window_size}] "
              f"Accuracy={accuracy}% Confidence={prediction_confidence:.3f}")
        print(f" Feature means: CPU={summary['cpu']}, MEM={summary['mem']}, PROC={summary['proc']}")
        print(f" Feature min  : CPU={summary['cpu_min']}, MEM={summary['mem_min']}, PROC={summary['proc_min']}")
        print(f" Feature max  : CPU={summary['cpu_max']}, MEM={summary['mem_max']}, PROC={summary['proc_max']}\n")

        time.sleep(sleep_sec)

if __name__ == "__main__":
    try:
        main_loop(window_size=5, iterations=20, sleep_sec=1)
    except KeyboardInterrupt:
        print("\n[Program terminated by user]")
    except Exception as e:
        print(f"[Fatal Error] {e}")