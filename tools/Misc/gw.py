import psutil
import random
import time
import sys
import logging
from collections import deque

# -------------------------------
# CONFIGURATION
# -------------------------------
WINDOW_SIZE = 5           # Sliding window size
ITERATIONS = 50           # Total iterations
SLEEP_SEC = 1             # Seconds between samples
CPU_KILL_THRESHOLD = 10   # Kill processes above this CPU %
MEM_KILL_THRESHOLD = 10   # Kill processes above this MEM %
AUTO_KILL = False         # Set True to auto kill heavy processes
LOG_FILE = "metrics.log"  # Log file

# -------------------------------
# Logging setup
# -------------------------------
logging.basicConfig(filename=LOG_FILE, level=logging.INFO, 
                    format='%(asctime)s - %(message)s')

# -------------------------------
# RNG setup
# -------------------------------
def real_rng():
    """Real RNG for predictions"""
    return random.random()

# -------------------------------
# Metrics collection
# -------------------------------
def get_cpu_usage():
    try:
        return psutil.cpu_percent(interval=0.5)
    except Exception as e:
        logging.error(f"CPU Error: {e}")
        return 0.0

def get_memory_usage():
    try:
        mem = psutil.virtual_memory()
        used_mb = (mem.total - mem.available) / (1024*1024)
        total_mb = mem.total / (1024*1024)
        return round(used_mb, 2), round(total_mb, 2)
    except Exception as e:
        logging.error(f"Memory Error: {e}")
        return 0.0, 0.0

def get_process_info():
    process_list = []
    try:
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            info = proc.info
            process_list.append({
                'pid': info['pid'],
                'name': info['name'],
                'cpu': info['cpu_percent'],
                'mem': info['memory_percent']
            })
    except Exception as e:
        logging.error(f"Process Error: {e}")
    return process_list

# -------------------------------
# Metrics Window
# -------------------------------
class MetricsWindow:
    def __init__(self, size=WINDOW_SIZE):
        self.size = size
        self.cpu = deque(maxlen=size)
        self.mem = deque(maxlen=size)
        self.proc = deque(maxlen=size)

    def add(self, cpu_val, mem_val, proc_val):
        self.cpu.append(cpu_val)
        self.mem.append(mem_val)
        self.proc.append(proc_val)

    def summary(self):
        if not self.cpu:
            return {}
        return {
            'cpu_mean': round(sum(self.cpu)/len(self.cpu),2),
            'cpu_min': min(self.cpu),
            'cpu_max': max(self.cpu),
            'mem_mean': round(sum(self.mem)/len(self.mem),2),
            'mem_min': min(self.mem),
            'mem_max': max(self.mem),
            'proc_mean': round(sum(self.proc)/len(self.proc),2),
            'proc_min': min(self.proc),
            'proc_max': max(self.proc)
        }

# -------------------------------
# Background process management
# -------------------------------
def identify_heavy_processes(process_list, cpu_threshold=CPU_KILL_THRESHOLD, mem_threshold=MEM_KILL_THRESHOLD):
    heavy = []
    for proc in process_list:
        if proc['cpu'] >= cpu_threshold or proc['mem'] >= mem_threshold:
            heavy.append(proc)
    return heavy

def handle_heavy_processes(heavy_processes):
    if not heavy_processes:
        print("[Background] No heavy processes detected.\n")
        return
    print("[Background] Heavy processes detected:")
    for proc in heavy_processes:
        print(f" PID={proc['pid']} Name={proc['name']} CPU={proc['cpu']}% MEM={proc['mem']:.1f}%")
        if AUTO_KILL:
            try:
                psutil.Process(proc['pid']).kill()
                print(f"   -> Auto-killed {proc['name']} (PID {proc['pid']})")
            except Exception as e:
                logging.error(f"Failed to kill PID {proc['pid']}: {e}")
    print()

# -------------------------------
# Main loop
# -------------------------------
def main_loop():
    window = MetricsWindow()
    for i in range(ITERATIONS):
        # Collect metrics
        cpu = get_cpu_usage()
        mem_used, mem_total = get_memory_usage()
        processes = get_process_info()
        proc_count = len(processes)

        # Add to window
        window.add(cpu, mem_used, proc_count)
        summary = window.summary()

        # Background process handling
        heavy_procs = identify_heavy_processes(processes)
        handle_heavy_processes(heavy_procs)

        # Prediction simulation
        confidence = real_rng()
        accuracy = round(confidence * 100,2)

        # Output
        print(f"[Window {i+1}/{ITERATIONS}] Accuracy={accuracy}% Confidence={confidence:.3f}")
        print(f" Feature means: CPU={summary['cpu_mean']} MEM={summary['mem_mean']} PROC={summary['proc_mean']}")
        print(f" Feature min  : CPU={summary['cpu_min']} MEM={summary['mem_min']} PROC={summary['proc_min']}")
        print(f" Feature max  : CPU={summary['cpu_max']} MEM={summary['mem_max']} PROC={summary['proc_max']}\n")

        # Log metrics
        logging.info(f"Iteration {i+1}: CPU={cpu} MEM={mem_used} PROC={proc_count} Acc={accuracy}")

        time.sleep(SLEEP_SEC)

# -------------------------------
# Entry
# -------------------------------
if __name__ == "__main__":
    try:
        main_loop()
    except KeyboardInterrupt:
        print("\n[Program terminated by user]")
    except Exception as e:
        logging.error(f"Fatal Error: {e}")
        print(f"[Fatal Error] {e}")