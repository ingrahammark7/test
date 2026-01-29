import random
import time

# Use hardware RNG
rng = random.SystemRandom()

# Function to get memory info from /proc/meminfo (Android/Linux)
def get_memory():
    try:
        meminfo = {}
        with open("/proc/meminfo") as f:
            for line in f:
                parts = line.split()
                key = parts[0].rstrip(':')
                value = int(parts[1])
                meminfo[key] = value  # in kB
        total = meminfo.get("MemTotal", 0) / 1024  # MB
        free = meminfo.get("MemFree", 0) / 1024
        available = meminfo.get("MemAvailable", 0) / 1024
        used = total - free
        return total, used, available
    except Exception:
        return 0.0, 0.0, 0.0

# Function to get CPU usage from /proc/stat
def get_cpu():
    try:
        with open("/proc/stat") as f:
            line = f.readline()
        parts = line.split()
        if parts[0] != 'cpu':
            return 0.0
        vals = list(map(int, parts[1:]))
        idle = vals[3] + vals[4]  # idle + iowait
        total = sum(vals)
        return idle, total
    except Exception:
        return None, None

# Track previous CPU for delta
prev_idle, prev_total = get_cpu()

# Simulation parameters
iterations = 20

print(f"Starting simulation: {iterations} iterations")
for i in range(1, iterations+1):
    # RNG value
    val = rng.random()
    
    # Simple "WinProb" function (example: direct mapping)
    win_prob = val  # can replace with more complex model
    
    # Memory stats
    total_mem, used_mem, avail_mem = get_memory()
    
    # CPU usage calculation
    idle, total = get_cpu()
    cpu_percent = 0.0
    if idle is not None and prev_idle is not None and total is not None and prev_total is not None:
        cpu_percent = 100.0 * (1 - (idle - prev_idle) / (total - prev_total))
        prev_idle, prev_total = idle, total
    
    # Python memory (approximation)
    python_mem = 0.0  # could use sys.getsizeof() if needed
    
    # Log iteration
    print(f"[Iteration {i}/{iterations}] CPU={cpu_percent:.2f}%, Mem={total_mem:.2f}/{used_mem:.2f}/{avail_mem:.2f} MB, Python Mem={python_mem:.2f} MB, RNG={val:.6f}, WinProb={win_prob:.3f}")
    
    time.sleep(0.05)  # small delay for realism

print("\n[Program finished]")