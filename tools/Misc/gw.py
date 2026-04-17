import os
import zipfile
import requests
import shapefile
import numpy as np
import networkx as nx

# Optional (best case)
try:
    from shapely.geometry import shape as shp_shape
    SHAPELY = True
except:
    SHAPELY = False

TIGER_URL = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"

# FLAT CWD ONLY
ZIP_FILE = "tl_2023_us_county.zip"
SHP_FILE = "tl_2023_us_county.shp"
EDGE_CACHE = "county_edges.npy"


# -----------------------------
# 1. Download + extract (once)
# -----------------------------
def ensure_data():
    if os.path.exists(SHP_FILE):
        return

    if not os.path.exists(ZIP_FILE):
        print("⬇ downloading TIGER...")
        r = requests.get(TIGER_URL, stream=True)
        r.raise_for_status()

        with open(ZIP_FILE, "wb") as f:
            for chunk in r.iter_content(1024 * 1024):
                if chunk:
                    f.write(chunk)

    print("📦 extracting...")
    with zipfile.ZipFile(ZIP_FILE, "r") as z:
        z.extractall(".")


# -----------------------------
# 2. Load shapes
# -----------------------------
def load_shapes():
    sf = shapefile.Reader(SHP_FILE)
    return sf.shapes()


# -----------------------------
# 3. Build adjacency (cached)
# -----------------------------
def build_graph(shapes):
    n = len(shapes)
    G = nx.Graph()
    G.add_nodes_from(range(n))

    # load cached edges if available
    if os.path.exists(EDGE_CACHE):
        print("✔ loading cached edges")
        edges = np.load(EDGE_CACHE, allow_pickle=True)
        G.add_edges_from(edges)
        print(f"✔ graph: {n} nodes, {G.number_of_edges()} edges (cached)")
        return G

    print("🔗 building adjacency (first run only)...")

    edges = []

    for i in range(n):
        si = shapes[i]

        # convert once if shapely available
        gi = shp_shape(si.__geo_interface__) if SHAPELY else None
        bi = si.bbox

        for j in range(i + 1, n):
            sj = shapes[j]
            bj = sj.bbox

            # fast reject
            if (bi[2] < bj[0] or bj[2] < bi[0] or
                bi[3] < bj[1] or bj[3] < bi[1]):
                continue

            if SHAPELY:
                gj = shp_shape(sj.__geo_interface__)
                if gi.touches(gj):
                    edges.append((i, j))
            else:
                # fallback approximation
                edges.append((i, j))

    np.save(EDGE_CACHE, np.array(edges, dtype=object))
    G.add_edges_from(edges)

    print(f"✔ graph built: {n} nodes, {len(edges)} edges")
    return G


# -----------------------------
# 4. State
# -----------------------------
def init_state(n):
    return (
        np.random.uniform(0.6, 1.0, n),  # H
        np.random.uniform(0.6, 1.0, n),  # I
        np.random.uniform(0.0, 0.2, n)   # P
    )


# -----------------------------
# 5. Dynamics
# -----------------------------
def step(G, H, I, P, params):
    alpha, beta, gamma, delta = params
    n = len(H)

    Hn = np.zeros(n)
    In = np.zeros(n)
    Pn = np.zeros(n)

    for i in range(n):
        neigh = list(G.neighbors(i))

        Pavg = np.mean(P[neigh]) if neigh else P[i]
        C = H[i] * I[i]

        Pn[i] = np.clip(P[i] + alpha*(1 - C) + 0.2*Pavg - beta*P[i], 0, 1)
        Hn[i] = np.clip(H[i] - gamma*P[i]*H[i], 0, 1)
        In[i] = np.clip(I[i] - delta*P[i]*I[i], 0, 1)

    return Hn, In, Pn


# -----------------------------
# 6. Phase metric
# -----------------------------
def giant_component(G, H, I, theta=0.25):
    C = H * I
    viable = [i for i in G.nodes if C[i] > theta]

    SG = G.subgraph(viable)

    if len(viable) == 0:
        return 0.0

    comps = list(nx.connected_components(SG))
    return max(len(c) for c in comps) / len(G)


# -----------------------------
# 7. Run
# -----------------------------
def run(T=120):
    ensure_data()
    shapes = load_shapes()
    G = build_graph(shapes)

    H, I, P = init_state(len(G))
    params = (0.6, 0.25, 0.8, 0.7)

    series = []

    for t in range(T):
        H, I, P = step(G, H, I, P, params)
        series.append(giant_component(G, H, I))

    return series


# -----------------------------
# 8. Execute
# -----------------------------
if __name__ == "__main__":
    import matplotlib.pyplot as plt

    s = run()

    plt.plot(s)
    plt.title("US County System (improved TIGER model)")
    plt.xlabel("Time")
    plt.ylabel("Giant Component")
    plt.show()