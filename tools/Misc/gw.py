import cv2
import numpy as np
from geomdl import NURBS
import matplotlib.pyplot as plt
import os

# ------------------------------
# Module 1: Load diagram and extract contours deterministically
# ------------------------------
def load_and_extract_contour(path, num_points=100):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    # Threshold
    _, bin_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    # Find external contours
    contours, _ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours) == 0:
        return np.zeros((num_points,2))
    # Take largest contour
    contour = max(contours, key=lambda x: cv2.contourArea(x))
    contour = contour[:,0,:]  # remove extra dimension
    # Normalize to [0,1]
    contour = contour - contour.min(axis=0)
    contour = contour / contour.max(axis=0)
    # Resample deterministically
    indices = np.linspace(0, len(contour)-1, num_points).astype(int)
    resampled = contour[indices]
    return resampled

# ------------------------------
# Module 2: Generate 3D points deterministically
# ------------------------------
def generate_3d_points(top_pts, side_pts, front_pts):
    num_points = min(len(top_pts), len(side_pts), len(front_pts))
    vertices = []
    for i in range(num_points):
        x = top_pts[i,0]
        y = top_pts[i,1]
        z = side_pts[i,1]  # side view: vertical axis = z
        vertices.append([x, y, z])
    return np.array(vertices)

# ------------------------------
# Module 3: Apply symmetry, twist, taper
# ------------------------------
def apply_symmetry(vertices, axis=0):
    mirrored = vertices.copy()
    mirrored[:,axis] *= -1
    return np.vstack([vertices, mirrored])

# ------------------------------
# Module 4: Loft NURBS surface
# ------------------------------
def loft_nurbs_surface(curve1_pts, curve2_pts):
    surf = NURBS.Surface()
    surf.degree_u = 3
    surf.degree_v = 3
    n = min(len(curve1_pts), len(curve2_pts))
    ctrlpts = []
    for i in range(n):
        row = (curve1_pts[i] + curve2_pts[i])/2
        ctrlpts.append(row.tolist())
    surf.set_ctrlpts(ctrlpts, size_u=len(ctrlpts), size_v=len(ctrlpts[0]))
    surf.knotvector_u = [0]*4 + [1]*4
    surf.knotvector_v = [0]*4 + [1]*4
    return surf

# ------------------------------
# Module 5: Visualize with matplotlib
# ------------------------------
def visualize(vertices):
    vertices = np.array(vertices,dtype=float)
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.scatter(vertices[:,0], vertices[:,1], vertices[:,2], c='r', s=10)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.show()

# ------------------------------
# Module 6: Export OBJ
# ------------------------------
def export_obj(vertices, filename="model.obj"):
    with open(filename,"w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

# ------------------------------
# Module 7: Full deterministic workflow
# ------------------------------
def process_aircraft(top_path, side_path, front_path, num_points=100):
    top_pts = load_and_extract_contour(top_path, num_points)
    side_pts = load_and_extract_contour(side_path, num_points)
    front_pts = load_and_extract_contour(front_path, num_points)
    vertices = generate_3d_points(top_pts, side_pts, front_pts)
    vertices = apply_symmetry(vertices)  # optional
    visualize(vertices)
    export_obj(vertices, filename=os.path.basename(top_path).replace(".png",".obj"))

# ------------------------------
# Example usage
# ------------------------------
diagram_files = [("top_view.png","side_view.png","front_view.png")]
for top, side, front in diagram_files:
    process_aircraft(top, side, front)