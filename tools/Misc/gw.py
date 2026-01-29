import random
import time
import math
import collections

# ======================================
# RNG SOURCES
# ======================================

sys_rng = random.SystemRandom()
py_rng = random.Random(123456)   # deterministic attacker-controlled RNG

def combined_rng():
    """Blend multiple RNG sources"""
    a = sys_rng.random()
    b = py_rng.random()
    return (a + b) % 1.0, a, b


# ======================================
# SYSTEM METRICS
# ======================================

def get_memory():
    try:
        meminfo = {}
        with open("/proc/meminfo") as f:
            for line in f:
                k, v = line.split()[:2]
                meminfo[k.rstrip(":")] = int(v)
        total = meminfo["MemTotal"] / 1024
        free = meminfo["MemFree"] / 1024
        avail = meminfo["MemAvailable"] / 1024
        used = total - free
        return total, used, avail
    except Exception:
        return 0.0, 0.0, 0.0

def get_cpu():
    try:
        with open("/proc/stat") as f:
            parts = f.readline().split()
        vals = list(map(int, parts[1:]))
        idle = vals[3] + vals[4]
        total = sum(vals)
        return idle, total
    except Exception:
        return None, None


# ======================================
# ML CORE
# ======================================

def sigmoid(x):
    if x < -60: return 0.0
    if x > 60:  return 1.0
    return 1 / (1 + math.exp(-x))

class OnlineLogReg:
    def __init__(self, n, lr=0.05):
        self.w = [0.0] * n
        self.lr = lr

    def predict(self, x):
        return sigmoid(sum(w * xi for w, xi in zip(self.w, x)))

    def update(self, x, y):
        p = self.predict(x)
        err = y - p
        for i in range(len(self.w)):
            self.w[i] += self.lr * err * x[i]
        return p, err


# ======================================
# ENTROPY MONITOR
# ======================================

class EntropyWindow:
    def __init__(self, size=64):
        self.buf = collections.deque(maxlen=size)

    def add(self, x):
        self.buf.append(int(x * 256))

    def entropy(self):
        if len(self.buf) < 2:
            return 0.0
        counts = collections.Counter(self.buf)
        total = len(self.buf)
        ent = 0.0
        for c in counts.values():
            p = c / total
            ent -= p * math.log2(p)
        return ent


# ======================================
# DELAYED REWARD BUFFER
# ======================================

class DelayedReward:
    def __init__(self, delay=3):
        self.buf = collections.deque(maxlen=delay)

    def push(self, x, pred):
        self.buf.append((x, pred))

    def resolve(self, reward, model):
        for x, _ in self.buf:
            model.update(x, reward)
        self.buf.clear()


# ======================================
# SETUP
# ======================================

iterations = 50
sleep_time = 0.15

main_model = OnlineLogReg(7)
adv_model  = OnlineLogReg(7)   # attacker tries to predict RNG

entropy_monitor = EntropyWindow()
reward_pipe = DelayedReward(delay=4)

prev_idle, prev_total = get_cpu()

print("\n=== RNG APPLICATION DOMINANCE LAB ===\n")

# ======================================
# LOOP
# ======================================

for i in range(1, iterations + 1):

    mixed, hw, sw = combined_rng()
    entropy_monitor.add(mixed)

    total_mem, used_mem, avail_mem = get_memory()

    idle, total = get_cpu()
    cpu = 0.0
    if idle and prev_idle and total != prev_total:
        cpu = 100 * (1 - (idle - prev_idle) / (total - prev_total))
        prev_idle, prev_total = idle, total

    used_r = used_mem / total_mem if total_mem else 0.0
    avail_r = avail_mem / total_mem if total_mem else 0.0

    features = [
        1.0,
        mixed,
        cpu / 100.0,
        used_r,
        avail_r,
        hw,
        sw
    ]

    # MAIN MODEL prediction
    win_prob, _ = main_model.update(features, 0.0)
    reward_pipe.push(features, win_prob)

    # ADVERSARY tries to predict mixed RNG
    adv_pred, adv_err = adv_model.update(features, mixed)

    # Delayed reward: success if RNG > 0.5 after delay
    if i % reward_pipe.buf.maxlen == 0:
        reward = 1.0 if mixed > 0.5 else 0.0
        reward_pipe.resolve(reward, main_model)

    ent = entropy_monitor.entropy()

    print(
        f"[{i:02d}] "
        f"RNG={mixed:.5f} "
        f"CPU={cpu:5.1f}% "
        f"ENT={ent:4.2f} "
        f"WinP={win_prob:.3f} "
        f"ADVerr={abs(adv_err):.4f}"
    )

    time.sleep(sleep_time)

# ======================================
# RESULTS
# ======================================

print("\n--- FINAL WEIGHTS (MAIN MODEL) ---")
for i, w in enumerate(main_model.w):
    print(f"w[{i}] = {w:.6f}")

print("\n--- FINAL WEIGHTS (ADVERSARY) ---")
for i, w in enumerate(adv_model.w):
    print(f"a[{i}] = {w:.6f}")

print("\n[FINISHED]")