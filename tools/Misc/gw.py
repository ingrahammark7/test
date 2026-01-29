import os
import time
import random
import tracemalloc

# ----------------------------
# TRUE RNG
# ----------------------------
def true_rng():
    """Return a float in [0,1) from /dev/urandom (fallback to random)."""
    try:
        val = int.from_bytes(os.urandom(4), 'big')
        return val / 2**32
    except Exception:
        return random.random()

# ----------------------------
# MEMORY METRICS
# ----------------------------
def memory_metrics():
    """Return (total, used, available) memory in MB."""
    try:
        with open('/proc/meminfo') as f:
            info = f.read()
        mem_total = int(next(line for line in info.splitlines() if "MemTotal" in line).split()[1]) / 1024
        mem_free = int(next(line for line in info.splitlines() if "MemFree" in line).split()[1]) / 1024
        mem_avail = int(next(line for line in info.splitlines() if "MemAvailable" in line).split()[1]) / 1024
        mem_used = mem_total - mem_free
        return round(mem_total,2), round(mem_used,2), round(mem_avail,2)
    except Exception:
        return 0,0,0

def python_mem():
    """Return current Python memory usage in MB."""
    try:
        tracemalloc.start()
        current, _ = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return round(current / 1024 / 1024, 2)
    except Exception:
        return 0

# ----------------------------
# WIN PROBABILITY CALCULATION
# ----------------------------
def compute_win_prob(rng_val, mem_used, py_mem):
    """
    Dummy placeholder for your prediction model.
    Combines RNG + memory metrics to estimate a 'win probability'.
    Replace with your actual logic.
    """
    # Example heuristic: RNG weighted, less Python memory = better
    prob = rng_val * 0.7 + (1 / (1 + py_mem)) * 0.3
    return round(prob, 3)

# ----------------------------
# PREDICTION LOOP
# ----------------------------
def prediction_loop(iterations=20):
    for i in range(1, iterations+1):
        rng_val = true_rng()
        mem_total, mem_used, mem_avail = memory_metrics()
        py_mem = python_mem()
        win_prob = compute_win_prob(rng_val, mem_used, py_mem)
        
        print(f"[Iteration {i}/{iterations}] "
              f"Mem={mem_total}/{mem_used}/{mem_avail} MB, "
              f"Python Mem={py_mem} MB, RNG={rng_val:.6f}, "
              f"WinProb={win_prob}")
        
        # --- Optional: insert your model call here using win_prob ---
        time.sleep(0.2)  # adjust speed if needed

# ----------------------------
# RUN LOOP
# ----------------------------
if __name__ == "__main__":
    prediction_loop(20)