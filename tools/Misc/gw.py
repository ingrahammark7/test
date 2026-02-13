import numpy as np
from geomdl import NURBS
import matplotlib.pyplot as plt
import cv2
import os

# --- Airfoil templates (deterministic NACA 0012 example) ---
def naca_4digit(m=0, p=0, t=12, n_points=50):
    """Generate NACA 4-digit airfoil coordinates"""
    t = t/100
    x = np.linspace(0,1,n_points)
    yt = 5*t*(0.2969*np.sqrt(x)-0.1260*x-0.3516*x**2+0.2843*x**3-0.1015*x**4)
    return np.column_stack([x, yt])

# --- Fuselage template ---
def fuselage_profile(top_width, side_height, n_points=20):
    """Elliptical fuselage section"""
    theta = np.linspace(0, np.pi, n_points)
    x = top_width/2 * np.cos(theta)
    y = side_height/2 * np.sin(theta)
    return np.column_stack([x,y])

# --- Load contour deterministically ---
def load_and_resample(path, n_points=100):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, bin_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    contours,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours)==0: return np.zeros((n_points,2))
    c = max(contours,key=lambda x: cv2.contourArea(x))[:,0,:]
    indices = np.linspace(0,len(c)-1,n_points).astype(int)
    return c[indices]/c.max(axis=0)

# --- Loft vertices between two curves ---
def loft(curve1, curve2):
    n = min(len(curve1),len(curve2))
    verts=[]
    for i in range(n):
        verts.append((curve1[i]+curve2[i])/2)
    return np.array(verts)

# --- Generate deterministic wing ---
def generate_wing(span=1.0,chord=0.2,n_points=50):
    airfoil = naca_4digit(n_points=n_points)
    verts=[]
    for i in np.linspace(0,span,n_points):
        section = airfoil.copy()
        section[:,0] = section[:,0]*chord + i  # sweep along span
        verts.append(section)
    return np.vstack(verts)

# --- Generate deterministic fuselage ---
def generate_fuselage(length=1.0,top_width=0.2,side_height=0.2,n_sections=20):
    verts=[]
    for i in np.linspace(0,length,n_sections):
        section = fuselage_profile(top_width, side_height)
        section[:,0] += i  # move along x-axis
        verts.append(section)
    return np.vstack(verts)

# --- Visualize 3D vertices ---
def visualize(vertices):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(vertices[:,0],vertices[:,1],vertices[:,2],c='r',s=5)
    plt.show()

# --- Export OBJ ---
def export_obj(vertices,filename="model.obj"):
    with open(filename,"w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

# --- Full deterministic pipeline ---
def process_aircraft(top_path, side_path, front_path):
    # Load top/side/front for fuselage dimensions
    top = load_and_resample(top_path)
    side = load_and_resample(side_path)
    front = load_and_resample(front_path)
    # Extract deterministic fuselage dimensions
    fuselage_len = 1.0
    top_width = top[:,0].max()
    side_height = side[:,1].max()
    fuselage = generate_fuselage(fuselage_len,top_width,side_height)
    wing = generate_wing(span=0.5,chord=0.2)
    # Merge everything with dummy z for fuselage
    fuselage_3d = np.column_stack([fuselage[:,0],fuselage[:,1],np.zeros(len(fuselage))])
    wing_3d = np.column_stack([wing[:,0],np.zeros(len(wing)),wing[:,1]])
    vertices = np.vstack([fuselage_3d, wing_3d])
    visualize(vertices)
    export_obj(vertices,"aircraft.obj")

# --- Example usage ---
process_aircraft("top_view.png","side_view.png","front_view.png")