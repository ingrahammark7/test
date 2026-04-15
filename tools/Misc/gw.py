import os
import time

seen = set()

def state():
    x = int.from_bytes(os.urandom(8), "big")
    return x >> 10  # ~1024× reduction

samples = 0
start = time.time()

while True:
    s = state()

    if s in seen:
        print("DUPLICATE")
        print("samples:", samples)
        print("time:", time.time() - start)
        break

    seen.add(s)
    samples += 1

    if samples % 10000 == 0:
        print(samples)