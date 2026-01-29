import psutil
import time
import random
import statistics
from collections import deque

# ---------------- CONFIG ----------------
WINDOW_SIZE = 5           # sliding window size
SLEEP_INTERVAL = 0.5      # seconds between iterations
ENABLE_AUTO_KILL = False  # set True to auto-kill offending processes
TOP_N = 3                 # number of processes to flag
RANDOM_SEED = None        # None uses real RNG

# ---------------- INIT ----------------
if RANDOM_SEED is not None:
    random.seed(RANDOM_SEED)

window = deque(maxlen=WINDOW_SIZE)
history = []

# ---------------- FUNCTIONS ----------------
def get_system_metrics():
    """Return CPU%, MEM%, PROC count"""
    try:
        cpu = psutil.cpu_percent(interval=None)
        mem = psutil.virtual_memory().percent
        proc = len(psutil.pids())
        return cpu, mem, proc
    except Exception:
        return 0.0, 0.0, 0

def get_process_list():
    """Return list of processes with cpu and memory usage"""
    procs = []
    for p in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
        try:
            info = p.info
            procs.append(info)
        except Exception:
            continue
    return procs

def recommend_processes_to_kill(window_history):
    """
    Look for processes that appear correlated with lower accuracy
    For simplicity, we flag top CPU/MEM users in bad windows
    """
    offender_counts = {}
    for entry in window_history:
        for proc in entry.get('processes', []):
            key = (proc['pid'], proc['name'])
            offender_counts[key] = offender_counts.get(key, 0) + 1
    # Sort by frequency
    offenders = sorted(offender_counts.items(), key=lambda x: x[1], reverse=True)
    return offenders[:TOP_N]

# ---------------- MAIN LOOP ----------------
try:
    iteration = 0
    while True:
        iteration += 1
        cpu, mem, proc_count = get_system_metrics()
        
        # Simulate prediction accuracy using random for now
        accuracy = random.uniform(0.6, 1.0)
        
        # Capture running processes
        procs = get_process_list()
        
        # Append window entry
        window.append({
            'cpu': cpu,
            'mem': mem,
            'proc_count': proc_count,
            'accuracy': accuracy,
            'processes': procs
        })
        
        # Compute window statistics
        cpu_vals = [w['cpu'] for w in window]
        mem_vals = [w['mem'] for w in window]
        proc_vals = [w['proc_count'] for w in window]
        acc_vals = [w['accuracy'] for w in window]
        
        print(f"[Window {iteration}/{WINDOW_SIZE}] Accuracy={statistics.mean(acc_vals):.4f} "
              f"CPU={statistics.mean(cpu_vals):.2f} MEM={statistics.mean(mem_vals):.2f} PROC={statistics.mean(proc_vals):.2f}")
        
        # Every full window, check for process offenders
        if len(window) == WINDOW_SIZE:
            offenders = recommend_processes_to_kill(window)
            print("Top potential background offenders:")
            for (pid, name), count in offenders:
                print(f"PID {pid} ({name}) appeared {count} times in window")
                if ENABLE_AUTO_KILL:
                    try:
                        psutil.Process(pid).terminate()
                        print(f"Terminated {name} (PID {pid})")
                    except Exception:
                        pass
        
        time.sleep(SLEEP_INTERVAL)

except KeyboardInterrupt:
    print("\nProgram terminated by user.")