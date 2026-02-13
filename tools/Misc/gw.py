import numpy as np
import cv2
import matplotlib.pyplot as plt
import os

# --- Parametric NACA airfoil ---
def naca_4digit(m=0,p=0,t=12,n_points=50):
    t = t/100
    x = np.linspace(0,1,n_points)
    yt = 5*t*(0.2969*np.sqrt(x)-0.126*x-0.3516*x**2+0.2843*x**3-0.1015*x**4)
    return np.column_stack([x, yt])

# --- Elliptical fuselage profile ---
def fuselage_profile(width, height, n_points=20):
    theta = np.linspace(0, np.pi, n_points)
    x = width/2 * np.cos(theta)
    y = height/2 * np.sin(theta)
    return np.column_stack([x,y])

# --- Load and resample contour deterministically ---
def load_and_resample(path, n_points=100):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    _, bin_img = cv2.threshold(img,127,255,cv2.THRESH_BINARY_INV)
    contours,_ = cv2.findContours(bin_img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    if len(contours)==0:
        return np.zeros((n_points,2)), bin_img
    c = max(contours,key=lambda x: cv2.contourArea(x))[:,0,:]
    indices = np.linspace(0,len(c)-1,n_points).astype(int)
    return c[indices]/c.max(axis=0), bin_img

# --- Detect multiple wings with automatic span & chord scaling ---
def detect_wings_with_dimensions(top_bin, threshold=5):
    profile = np.sum(top_bin>0, axis=0)
    wings = []
    in_wing = False
    start = 0
    for i, val in enumerate(profile):
        if val > threshold and not in_wing:
            in_wing = True
            start = i
        elif val <= threshold and in_wing:
            in_wing = False
            span_idx = i - start
            chord_pixels = np.max(np.sum(top_bin[:,start:i]>0, axis=0))
            wings.append({'start': start, 'span': span_idx, 'chord': chord_pixels/100})
    if in_wing:
        span_idx = len(profile) - start
        chord_pixels = np.max(np.sum(top_bin[:,start:]>0, axis=0))
        wings.append({'start': start, 'span': span_idx, 'chord': chord_pixels/100})
    return wings

# --- Generate deterministic wing ---
def generate_wing(span=1.0,chord=0.2,n_points=50,sweep=0.0,dihedral=0.0,twist=0.0,offset_x=0.0,offset_y=0.0):
    airfoil = naca_4digit(n_points=n_points)
    verts=[]
    for i,s in enumerate(np.linspace(0,span,n_points)):
        section = airfoil.copy()
        section[:,0] *= chord
        section[:,0] += offset_x + s*np.tan(np.radians(sweep))
        section[:,1] += offset_y + s*np.tan(np.radians(dihedral))
        rad = np.radians(twist*s/span)
        y,z = section[:,1],section[:,0]
        section[:,1] = y*np.cos(rad)-z*np.sin(rad)
        section[:,0] = y*np.sin(rad)+z*np.cos(rad)
        verts.append(section)
    return np.vstack(verts)

# --- Generate fuselage ---
def generate_fuselage(length=1.0,top_width=0.2,side_height=0.2,n_sections=20):
    verts=[]
    for i in np.linspace(0,length,n_sections):
        section = fuselage_profile(top_width,side_height)
        section[:,0] += i
        verts.append(section)
    return np.vstack(verts)

# --- Generate tailplane with scaling ---
def generate_tailplane(span=0.25,chord=0.1,n_points=20,dihedral=0.0,vertical=False,offset_x=0.0,offset_y=0.0):
    airfoil = naca_4digit(n_points=n_points)
    verts=[]
    for i,s in enumerate(np.linspace(0,span,n_points)):
        section = airfoil.copy()
        section[:,0] *= chord
        if vertical:
            section_3d = np.column_stack([np.zeros(len(section))+offset_x, section[:,0]+offset_y, section[:,1]])
        else:
            section_3d = np.column_stack([section[:,0]+offset_x, np.zeros(len(section))+offset_y, section[:,1]])
        section_3d[:,1 if not vertical else 0] += s*np.tan(np.radians(dihedral))
        verts.append(section_3d)
    return np.vstack(verts)

# --- Visualization ---
def visualize(vertices):
    fig = plt.figure()
    ax = fig.add_subplot(111,projection='3d')
    ax.scatter(vertices[:,0],vertices[:,1],vertices[:,2],c='r',s=5)
    plt.show()

# --- OBJ export ---
def export_obj(vertices,filename="aircraft.obj"):
    with open(filename,"w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

# --- Full deterministic multi-wing aircraft pipeline ---
def process_aircraft(top_path, side_path, front_path):
    top_pts, top_bin = load_and_resample(top_path)
    side_pts, side_bin = load_and_resample(side_path)
    
    # --- Fuselage ---
    fuselage_len = 1.0
    top_width = top_pts[:,0].max()
    side_height = side_pts[:,1].max()
    fuselage = generate_fuselage(fuselage_len, top_width, side_height)
    fuselage_3d = np.column_stack([fuselage[:,0], fuselage[:,1], np.zeros(len(fuselage))])
    
    # --- Wings ---
    wing_regions = detect_wings_with_dimensions(top_bin)
    wings_3d = []
    for wing in wing_regions:
        wing_mesh = generate_wing(
            span=wing['span']/100,
            chord=wing['chord'],  # auto-scaled chord
            sweep=10,
            dihedral=5,
            twist=5,
            offset_x=wing['start']/100
        )
        wing_3d = np.column_stack([wing_mesh[:,0], np.zeros(len(wing_mesh)), wing_mesh[:,1]])
        wings_3d.append(wing_3d)
    
    # --- Tailplanes (scaled) ---
    tail_h = generate_tailplane(
        span=top_width*0.25, 
        chord=side_height*0.5,
        dihedral=2,
        vertical=False,
        offset_x=fuselage_len*0.75
    )
    tail_v = generate_tailplane(
        span=side_height*0.2, 
        chord=side_height*0.3,
        dihedral=0,
        vertical=True,
        offset_x=fuselage_len*0.75
    )
    
    # --- Merge all vertices ---
    vertices = fuselage_3d
    for w in wings_3d:
        vertices = np.vstack([vertices, w])
    vertices = np.vstack([vertices, tail_h, tail_v])
    
    # --- Visualize and export ---
    visualize(vertices)
    export_obj(vertices,"aircraft.obj")

# --- Example usage ---
process_aircraft("top_view.png","side_view.png","front_view.png")