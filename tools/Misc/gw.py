import os
import random
import time

# --- Android-friendly memory read ---
def get_mem():
    """Return (total, free, used) memory in MB using /proc/meminfo."""
    try:
        meminfo = {}
        with open("/proc/meminfo", "r") as f:
            for line in f:
                key, val = line.split(":", 1)
                meminfo[key.strip()] = int(val.strip().split()[0])
        total = meminfo.get("MemTotal", 0) / 1024  # kB -> MB
        free = meminfo.get("MemFree", 0) / 1024
        cached = meminfo.get("Cached", 0) / 1024
        used = total - free - cached
        return total, free, used
    except Exception:
        return 0, 0, 0

# --- Python memory (best-effort) ---
def get_python_mem():
    try:
        import tracemalloc
        if not tracemalloc.is_tracing():
            tracemalloc.start()
        current, peak = tracemalloc.get_traced_memory()
        return current / 1024 / 1024  # bytes -> MB
    except Exception:
        return 0.0

# --- Real RNG (Android-compatible) ---
def real_rng():
    try:
        # Use os.urandom for strong randomness
        return int.from_bytes(os.urandom(8), "big") / 2**64
    except Exception:
        # fallback to random.random if urandom fails
        return random.random()

# --- Win probability function ---
def calc_win_prob(rng):
    """Map RNG to a realistic win probability [0.0,1.0]"""
    # can use cubic scaling to exaggerate extremes
    return min(max(rng**0.7, 0.0), 1.0)

# --- Main loop ---
def main(iterations=20):
    print(f"Starting simulation: {iterations} iterations")
    for i in range(1, iterations + 1):
        total, free, used = get_mem()
        py_mem = get_python_mem()
        rng_val = real_rng()
        win_prob = calc_win_prob(rng_val)

        print(f"[Iteration {i}/{iterations}] "
              f"Mem={total:.2f}/{free:.2f}/{used:.2f} MB, "
              f"Python Mem={py_mem:.2f} MB, "
              f"RNG={rng_val:.6f}, WinProb={win_prob:.3f}")

        # Optional: minimal sleep for system stability
        time.sleep(0.05)

if __name__ == "__main__":
    main()