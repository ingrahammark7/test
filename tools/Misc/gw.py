import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.stats import lognorm, gamma, expon

# -----------------------------
# 1) Build a synthetic road+rail graph
# -----------------------------
def build_synthetic_graph():
    G = nx.DiGraph()

    # Add nodes (cities, industrial zones, Donbass boundary)
    # In a real model, you would use actual map data.
    nodes = [
        ("Moscow", {"type": "industrial"}),
        ("StPetersburg", {"type": "industrial"}),
        ("Kursk", {"type": "industrial"}),
        ("Rostov", {"type": "industrial"}),
        ("Donbass", {"type": "target"}),
    ]
    G.add_nodes_from(nodes)

    # Add edges: (u, v, distance_km, speed_limit_kmh, capacity_veh_per_hr, road_factor)
    # road_factor is a multiplier to speed to represent terrain/quality
    edges = [
        ("Moscow", "Kursk", 700, 90, 1000, 0.9),
        ("Moscow", "Rostov", 1200, 90, 800, 0.8),
        ("StPetersburg", "Moscow", 700, 100, 900, 0.9),
        ("Kursk", "Donbass", 600, 80, 600, 0.8),
        ("Rostov", "Donbass", 400, 80, 700, 0.85),
        ("Rostov", "Kursk", 500, 80, 500, 0.75),
    ]

    for u, v, dist, speed, cap, factor in edges:
        G.add_edge(u, v, distance=dist, speed_limit=speed,
                   capacity=cap, road_factor=factor, type="road")

    # Add rail edges
    rail_edges = [
        ("Moscow", "Donbass", 1200, 120, 2000, 0.95),
        ("StPetersburg", "Donbass", 1400, 120, 1800, 0.95),
    ]
    for u, v, dist, speed, cap, factor in rail_edges:
        G.add_edge(u, v, distance=dist, speed_limit=speed,
                   capacity=cap, road_factor=factor, type="rail")

    return G

G = build_synthetic_graph()

# -----------------------------
# 2) Model parameters (plausible values)
# -----------------------------
N_MAX = 3000  # max vehicles (upper bound)

# Mobilization delay (days) - Gamma distribution
MOB_K = 3.0
MOB_THETA = 2.0

# Speed distribution (km/h) - lognormal
# mean speed around 40 km/h with realistic variance
SPEED_MU = np.log(40)
SPEED_SIGMA = 0.4

# Tactical delay (hours) - Exponential
TAC_LAMBDA = 0.2

# Ukraine capability model
# Ukraine front advance speed (km/day) depends on net advantage
K_MAX_ADVANCE = 10.0  # max advance rate (option 2: realistic)
ALPHA = 0.05

# Ukraine and Russia capability (logistic ramp)
U0 = 0.8
R0 = 1.0
TAU_U = 5.0
TAU_R = 3.0
SIGMA_U = 4.0
SIGMA_R = 6.0

# Simulation
N_SIM = 20000
TIME_HORIZON_DAYS = 30
TIME_STEP = 0.5

# Donbass target node
TARGET_NODE = "Donbass"

# -----------------------------
# 3) Helper functions
# -----------------------------
def logistic(t, t0, sigma):
    return 1.0 / (1.0 + np.exp(-(t - t0) / sigma))

def ukraine_advantage(t):
    # Ukraine and Russia capability over time
    FU = U0 * logistic(t, TAU_U, SIGMA_U)
    FR = R0 * logistic(t, TAU_R, SIGMA_R)
    return FU - FR

def front_speed(t):
    # front speed as tanh of advantage
    adv = ukraine_advantage(t)
    return K_MAX_ADVANCE * np.tanh(ALPHA * adv)

def route_travel_time(G, route):
    # Compute travel time in hours along a route
    total_hours = 0.0
    for u, v in zip(route[:-1], route[1:]):
        edge = G[u][v]
        dist = edge["distance"]
        speed_limit = edge["speed_limit"]
        factor = edge["road_factor"]

        # sample speed from lognormal
        speed = lognorm(s=SPEED_SIGMA, scale=np.exp(SPEED_MU)).rvs()
        speed = min(speed, speed_limit)  # cannot exceed speed limit

        travel_time_hours = dist / (speed * factor)
        total_hours += travel_time_hours

        # add tactical delay
        tactical_delay = expon(scale=1.0 / TAC_LAMBDA).rvs()
        total_hours += tactical_delay

    return total_hours

# -----------------------------
# 4) Main simulation
# -----------------------------
def simulate_arrival():
    # Precompute all shortest paths from industrial zones to Donbass
    sources = [n for n, d in G.nodes(data=True) if d["type"] == "industrial"]
    routes = {}
    for s in sources:
        try:
            routes[s] = nx.shortest_path(G, s, TARGET_NODE, weight="distance")
        except nx.NetworkXNoPath:
            continue

    arrival_times = []

    for _ in range(N_SIM):
        # Sample number of vehicles
        n_vehicles = np.random.randint(1, N_MAX + 1)

        # Sample mobilization delay (days)
        mobilization_days = gamma(a=MOB_K, scale=MOB_THETA).rvs()

        # Choose random source
        src = np.random.choice(sources)
        route = routes[src]

        # Compute travel time hours
        travel_hours = route_travel_time(G, route)
        travel_days = travel_hours / 24.0

        # Total Russian arrival time
        T_R = mobilization_days + travel_days

        # Compute front blocking time for the route
        # Estimate distance to front at start and advance over time
        route_distance_km = sum(G[u][v]["distance"] for u, v in zip(route[:-1], route[1:]))
        # If front speed is average over time, approximate block time
        # We approximate the front reaching the route midpoint
        midpoint = route_distance_km / 2.0

        # Integrate front speed over time to find blocking time (simple numerical)
        t = 0.0
        distance_covered = 0.0
        dt = 0.1
        while distance_covered < midpoint and t < TIME_HORIZON_DAYS:
            distance_covered += front_speed(t) * dt
            t += dt

        T_U = t  # time when front reaches midpoint

        # Effective arrival if Russian arrives before the front blocks
        if T_R < T_U:
            arrival_times.append(T_R)

    return arrival_times

arrival_times = simulate_arrival()

# -----------------------------
# 5) Output results
# -----------------------------
arrival_times = np.array(arrival_times)
arrival_times.sort()

# Probability curve
time_grid = np.arange(0, TIME_HORIZON_DAYS + TIME_STEP, TIME_STEP)
prob_curve = []
for t in time_grid:
    prob_curve.append(np.mean(arrival_times <= t))

# Plot
plt.plot(time_grid, prob_curve)
plt.xlabel("Days")
plt.ylabel("Probability of Effective Arrival")
plt.title("Probability of Russian Ground Vehicles Arriving in Donbass")
plt.grid(True)
plt.show()

# Key statistics
if len(arrival_times) > 0:
    print("Earliest effective arrival (days):", arrival_times[0])
    print("Median effective arrival (days):", np.median(arrival_times))
    print("Latest effective arrival (days):", arrival_times[-1])
    print("Peak probability time (approx):", time_grid[np.argmax(prob_curve)])
else:
    print("No effective arrivals in simulation (Ukraine blocks all).")