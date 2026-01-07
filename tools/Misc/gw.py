import random

# Parameters
N = 10_000   # initial drones
S = 100      # shooters
kps = 1      # kills per shooter per second
T = 200      # total seconds
seed = 1

# Initialize
random.seed(seed)
drones = set(range(N))

print(f"Time\tKills\tDrones_Remaining")

for t in range(T):
    if not drones:
        print(f"All drones destroyed at second {t}")
        break

    shots = S * kps
    drone_list = list(drones)
    L = len(drone_list)

    # Select targets randomly
    targets = [drone_list[random.randrange(L)] for _ in range(shots)]

    # Only unique kills count
    kills = set(targets)
    drones -= kills

    print(f"{t+1}\t{len(kills)}\t{len(drones)}")