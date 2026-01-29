import subprocess
import time
import random
import numpy as np
from collections import deque

# -----------------------------
# Robust Android Metrics
# -----------------------------
def read_metrics():
    cpu = 0.0
    mem = 0.0
    proc = 0
    try:
        # CPU usage %
        top_output = subprocess.check_output("top -n 1", shell=True, stderr=subprocess.DEVNULL).decode()
        cpu_line = next((line for line in top_output.splitlines() if "Cpu" in line or "CPU" in line), None)
        if cpu_line:
            try:
                cpu = float(cpu_line.split()[1].replace('%', '')) / 100.0 - 0.5
            except:
                cpu = 0.0
    except:
        cpu = 0.0

    try:
        # MEM usage MB
        mem_line = subprocess.check_output("cat /proc/meminfo", shell=True, stderr=subprocess.DEVNULL).decode()
        mem_avail_line = next((line for line in mem_line.splitlines() if "MemAvailable" in line), None)
        if mem_avail_line:
            try:
                mem = int(mem_avail_line.split()[1]) / 1024  # MB
            except:
                mem = 0.0
    except:
        mem = 0.0

    try:
        # Process count
        proc_line = subprocess.check_output("ps | wc -l", shell=True, stderr=subprocess.DEVNULL).decode()
        proc = int(proc_line.strip())
    except:
        proc = 0

    return cpu, mem, proc


# -----------------------------
# Robust Background Killer
# -----------------------------
def kill_background(threshold_cpu=0.01):
    try:
        processes = subprocess.check_output("ps -eo pid,ni,comm,%cpu", shell=True, stderr=subprocess.DEVNULL).decode().splitlines()[1:]
        for proc_info in processes:
            try:
                pid, nice, comm, cpu_percent = proc_info.split(None, 3)
                pid = int(pid)
                nice = int(nice)
                cpu_percent = float(cpu_percent)
                if nice > 5 and cpu_percent/100.0 < threshold_cpu:
                    subprocess.run(["kill", "-9", str(pid)], stderr=subprocess.DEVNULL)
            except:
                continue
    except:
        pass


# -----------------------------
# Feature Window
# -----------------------------
class FeatureWindow:
    def __init__(self, size=5):
        self.size = size
        self.window = deque(maxlen=size)

    def add(self, feature):
        self.window.append(feature)

    def get_mean(self):
        if not self.window:
            return [0.0, 0.0, 0.0]
        arr = np.array(self.window)
        return arr.mean(axis=0)

    def get_min(self):
        if not self.window:
            return [0.0, 0.0, 0.0]
        arr = np.array(self.window)
        return arr.min(axis=0)

    def get_max(self):
        if not self.window:
            return [0.0, 0.0, 0.0]
        arr = np.array(self.window)
        return arr.max(axis=0)


# -----------------------------
# Prediction (dummy model)
# -----------------------------
def predict(feature_mean):
    # Example logic: higher MEM and lower CPU -> better prediction
    cpu, mem, proc = feature_mean
    score = 0.5 + mem/200 - cpu
    return min(max(score, 0.0), 1.0)


# -----------------------------
# Main Loop
# -----------------------------
def main(iterations=100, window_size=5):
    fw = FeatureWindow(size=window_size)
    random.seed()  # Use system RNG
    np.random.seed(int(time.time()))  # Real RNG

    for i in range(iterations):
        # Kill background occasionally for best performance
        if i % 10 == 0:
            kill_background()

        # Read metrics safely
        cpu, mem, proc = read_metrics()
        fw.add([cpu, mem, proc])

        # Compute features
        feature_mean = fw.get_mean()
        feature_min = fw.get_min()
        feature_max = fw.get_max()

        # Make prediction
        score = predict(feature_mean)
        win = score > random.random()

        # Log output clearly
        print(f"[Iteration {i+1}/{iterations}, Window={window_size}] Win={win} Score={score:.3f}")
        print(f" Feature means: CPU={feature_mean[0]:.2f}, MEM={feature_mean[1]:.2f}, PROC={feature_mean[2]:.1f}")
        print(f" Feature min  : CPU={feature_min[0]:.2f}, MEM={feature_min[1]:.2f}, PROC={feature_min[2]:.1f}")
        print(f" Feature max  : CPU={feature_max[0]:.2f}, MEM={feature_max[1]:.2f}, PROC={feature_max[2]:.1f}")
        print("-"*60)

        # Wait a bit to avoid overloading system
        time.sleep(0.2)


if __name__ == "__main__":
    main(iterations=100, window_size=5)