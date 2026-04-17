import os
import io
import zipfile
import requests
import shapefile
import networkx as nx
import numpy as np

TIGER_URL = "https://www2.census.gov/geo/tiger/TIGER2023/COUNTY/tl_2023_us_county.zip"

# FLAT FILES ONLY (current working directory)
ZIP_PATH = "tl_2023_us_county.zip"
SHP_FILE = "tl_2023_us_county.shp"


# -----------------------------
# 1. Download + extract (CWD only)
# -----------------------------
def ensure_tiger_cached():
    # already extracted
    if os.path.exists(SHP_FILE):
        print("✔ Using cached TIGER shapefile (cwd)")
        return

    # download if missing
    if not os.path.exists(ZIP_PATH):
        print("⬇ Downloading TIGER counties (cwd only)...")
        r = requests.get(TIGER_URL, stream=True)
        r.raise_for_status()

        with open(ZIP_PATH, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024 * 1024):
                if chunk:
                    f.write(chunk)

    # extract EVERYTHING into cwd (flat)
    print("📦 Extracting into current directory (no folders)...")
    with zipfile.ZipFile(ZIP_PATH, "r") as z:
        z.extractall(".")

    print("✔ TIGER ready in cwd")


# -----------------------------
# 2. Load shapes
# -----------------------------
def load_shapes():
    sf = shapefile.Reader(SHP_FILE)
    return sf.shapes()


# -----------------------------
# 3. Build adjacency graph
# -----------------------------
def build_graph(shapes):
    n = len(shapes)
    G = nx.Graph()
    G.add_nodes_from(range(n))

    print("🔗 Building adjacency graph...")

    for i in range(n):
        bbox_i = shapes[i].bbox

        for j in range(i + 1, n):
            bbox_j = shapes[j].bbox

            # fast reject
            if (bbox_i[2] < bbox_j[0] or bbox_j[2] < bbox_i[0] or
                bbox_i[3] < bbox_j[1] or bbox_j[3] < bbox_i[1]):
                continue

            G.add_edge(i, j)

    print(f"✔ Graph built: {G.number_of_nodes()} nodes / {G.number_of_edges()} edges")
    return G


# -----------------------------
# 4. State init
# -----------------------------
def init_state(n):
    H = np.random.uniform(0.6, 1.0, n)
    I = np.random.uniform(0.6, 1.0, n)
    P = np.random.uniform(0.0, 0.2, n)
    return H, I, P


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
        P_avg = np.mean(P[neigh]) if neigh else P[i]

        C = H[i] * I[i]

        Pn[i] = np.clip(P[i] + alpha*(1 - C) + 0.2*P_avg - beta*P[i], 0, 1)
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
    ensure_tiger_cached()
    shapes = load_shapes()
    G = build_graph(shapes)

    n = len(G)
    H, I, P = init_state(n)

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

    series = run()

    plt.plot(series)
    plt.title("US County Collapse (flat CWD TIGER)")
    plt.xlabel("Time")
    plt.ylabel("Giant Component Fraction")
    plt.show()