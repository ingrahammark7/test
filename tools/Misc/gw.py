import cv2
import numpy as np
from geomdl import NURBS
import matplotlib.pyplot as plt
import os

# ------------------------------
# Module 1: Load & preprocess diagrams
# ------------------------------
def load_diagram(path, scale=1.0):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, bin_img = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY_INV)
    kernel = np.ones((3,3), np.uint8)
    bin_img = cv2.morphologyEx(bin_img, cv2.MORPH_OPEN, kernel)
    coords = np.column_stack(np.where(bin_img>0))
    if len(coords) == 0:
        return np.zeros((1,2)), bin_img
    min_vals = coords.min(axis=0)
    max_vals = coords.max(axis=0)
    coords = (coords - min_vals)/(max_vals - min_vals)*scale
    return coords, bin_img

# ------------------------------
# Module 2: Component segmentation
# ------------------------------
def segment_components(bin_img):
    num_labels, labels, stats, centroids = cv2.connectedComponentsWithStats(bin_img)
    components = []
    for i in range(1, num_labels):
        mask = (labels==i).astype(np.uint8)*255
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if contours:
            components.append(contours[0])
    return components

# ------------------------------
# Module 3: Contour -> spline
# ------------------------------
def contour_to_spline(contour):
    pts = np.array([p[0] for p in contour])
    if len(pts)<3: return pts
    from scipy.interpolate import splprep, splev
    tck, u = splprep(pts.T, s=0)
    u_new = np.linspace(0,1,len(pts)*2)
    x_new, y_new = splev(u_new, tck)
    return np.column_stack([x_new, y_new])

# ------------------------------
# Module 4: Degenerate 3D points
# ------------------------------
def generate_deg_points(components_2d, view_type):
    vertices = []
    for comp in components_2d:
        spline = contour_to_spline(comp)
        for pt in spline:
            if view_type=="top": vertices.append([pt[0], pt[1], None])
            if view_type=="side": vertices.append([pt[0], None, pt[1]])
            if view_type=="front": vertices.append([None, pt[0], pt[1]])
    return np.array(vertices,dtype=object)

# ------------------------------
# Module 5: Fill missing coordinates
# ------------------------------
def fill_missing(vertices, top_pts, side_pts, front_pts):
    for i,v in enumerate(vertices):
        if v[2] is None:
            match = min(side_pts, key=lambda s: abs(s[0]-v[0])) if v[0] is not None and len(side_pts)>0 else None
            if match is not None: v[2]=match[1]
        if v[1] is None:
            match = min(top_pts, key=lambda t: abs(t[0]-v[0])) if v[0] is not None and len(top_pts)>0 else None
            if match is not None: v[1]=match[1]
        if v[0] is None:
            match = min(front_pts, key=lambda f: abs(f[1]-v[2])) if v[2] is not None and len(front_pts)>0 else None
            if match is not None: v[0]=match[0]
        vertices[i] = v
    return vertices

# ------------------------------
# Module 6: Loft NURBS surface
# ------------------------------
def loft_nurbs_surface(curve1_pts, curve2_pts):
    surf = NURBS.Surface()
    surf.degree_u = 3
    surf.degree_v = 3
    n = min(len(curve1_pts), len(curve2_pts))
    ctrlpts = []
    for i in range(n):
        row = ((curve1_pts[i] if i<len(curve1_pts) else curve1_pts[-1]) +
               (curve2_pts[i] if i<len(curve2_pts) else curve2_pts[-1]))/2
        ctrlpts.append(row.tolist())
    surf.set_ctrlpts(ctrlpts, size_u=len(ctrlpts), size_v=len(ctrlpts[0]))
    surf.knotvector_u = [0]*4 + [1]*4
    surf.knotvector_v = [0]*4 + [1]*4
    return surf

# ------------------------------
# Module 7: Symmetry / Twist / Taper
# ------------------------------
def apply_symmetry(vertices, axis=0):
    mirrored = vertices.copy()
    mirrored[:,axis] *= -1
    return np.vstack([vertices, mirrored])

def apply_twist_taper(vertices, twist_deg=0, taper=1.0, axis=2):
    rad = np.deg2rad(twist_deg)
    for i,v in enumerate(vertices):
        factor = taper*(i/len(vertices))
        if axis==2:
            y,z = v[1], v[2]
            if y is not None and z is not None:
                v[1] = y*np.cos(rad*factor) - z*np.sin(rad*factor)
                v[2] = y*np.sin(rad*factor) + z*np.cos(rad*factor)
    return vertices

# ------------------------------
# Module 8: Airfoil insertion
# ------------------------------
def insert_airfoil(vertices, airfoil_pts, position=0):
    for i, pt in enumerate(airfoil_pts):
        vertices[position+i][0] = pt[0]
        vertices[position+i][1] = pt[1]
    return vertices

# ------------------------------
# Module 9: Matplotlib 3D visualization
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
# Module 10: OBJ export
# ------------------------------
def export_obj(vertices, filename="model.obj"):
    with open(filename,"w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

# ------------------------------
# Module 11: AI placeholder
# ------------------------------
def ai_predict_missing_features(vertices):
    return vertices

# ------------------------------
# Module 12: Full batch workflow
# ------------------------------
def process_aircraft(diagram_set):
    for top_path, side_path, front_path in diagram_set:
        top_pts, top_bin = load_diagram(top_path)
        side_pts, side_bin = load_diagram(side_path)
        front_pts, front_bin = load_diagram(front_path)
        top_comp = segment_components(top_bin)
        side_comp = segment_components(side_bin)
        front_comp = segment_components(front_bin)
        vertices = np.vstack([
            generate_deg_points(top_comp,"top"),
            generate_deg_points(side_comp,"side"),
            generate_deg_points(front_comp,"front")
        ])
        vertices = fill_missing(vertices, top_pts, side_pts, front_pts)
        vertices = apply_symmetry(vertices)
        vertices = ai_predict_missing_features(vertices)
        visualize(vertices)
        export_obj(vertices, filename=os.path.basename(top_path).replace(".png",".obj"))

# ------------------------------
# Example usage
# ------------------------------
diagram_files = [("tv.png","sv.png","fv.png")]
process_aircraft(diagram_files)