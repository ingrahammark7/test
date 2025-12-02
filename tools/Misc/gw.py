import numpy as np
import plotly.graph_objects as go
from ipywidgets import interact, VBox, FloatSlider, IntSlider, Dropdown

# ----------------------------
# Gel depth
# ----------------------------
depth = np.linspace(0, 0.6, 300)
baseline = 500 * np.exp(-((depth - 0.30)/0.10)**2)

# ----------------------------
# Grids for thickness and standoff
# ----------------------------
thicknesses = np.linspace(0.1, 1.5, 25)
standoffs = np.linspace(0.0, 0.6, 25)
X, Y = np.meshgrid(standoffs, thicknesses)  # Correct 2D grids for Surface

# ----------------------------
# Helper: compute deposition curve
# ----------------------------
def compute_curve(thickness, standoff, limb_absorption, perturb_factor, air_loss_factor):
    peak_depth = 0.30 - 0.15 * perturb_factor
    width = 0.10 + 0.05*np.clip((thickness-0.8)/0.5,0,1)
    amplitude = 500 * (1 - np.clip((thickness-0.8)/0.5,0,1))
    air_factor = 1 / (1 + (standoff/0.3)**2)
    curve = amplitude * np.exp(-((depth - peak_depth)/width)**2)
    curve *= air_factor * (1 - limb_absorption) * air_loss_factor
    return curve

def compute_peak_energy_grid(thicknesses, standoffs, limb_absorption, perturb_factor, air_loss_factor):
    Z = np.zeros((len(thicknesses), len(standoffs)))
    for i, t in enumerate(thicknesses):
        for j, s in enumerate(standoffs):
            Z[i,j] = compute_curve(t, s, limb_absorption, perturb_factor, air_loss_factor).max()
    return Z

# ----------------------------
# Interactive 3D animation
# ----------------------------
def interactive_3D(param_to_animate='perturbation', param_min=0.0, param_max=1.0, frames_count=10,
                   limb_absorption=0.5, air_loss_factor=1.0):
    
    param_values = np.linspace(param_min, max(param_min, param_max), frames_count)
    frames = []

    # Precompute frames
    for val in param_values:
        pd, la, al = 0.5, limb_absorption, air_loss_factor
        if param_to_animate == 'perturbation': pd = val
        elif param_to_animate == 'limb_absorption': la = val
        elif param_to_animate == 'air_loss_factor': al = val
        Z = compute_peak_energy_grid(thicknesses, standoffs, la, pd, al)
        frames.append(go.Frame(data=[go.Surface(z=Z, x=X, y=Y, colorscale='Viridis', cmin=0, cmax=500)],
                               name=f'{val:.4f}'))  # Unique frame names

    # Initial frame
    init_val = param_values[0]
    pd, la, al = 0.5, limb_absorption, air_loss_factor
    if param_to_animate == 'perturbation': pd = init_val
    elif param_to_animate == 'limb_absorption': la = init_val
    elif param_to_animate == 'air_loss_factor': al = init_val
    Z_init = compute_peak_energy_grid(thicknesses, standoffs, la, pd, al)

    fig = go.Figure(
        data=[go.Surface(z=Z_init, x=X, y=Y, colorscale='Viridis', cmin=0, cmax=500)],
        layout=go.Layout(
            title=f"3D Peak Energy Surface | {param_to_animate}={init_val:.2f}",
            scene=dict(
                xaxis=dict(title='Standoff (m)'),
                yaxis=dict(title='Thickness (HVL)'),
                zaxis=dict(title='Peak Energy (J/m)')
            ),
            updatemenus=[dict(
                type='buttons',
                buttons=[dict(label='Play', method='animate', args=[None, {"frame": {"duration":500,"redraw":True}, "fromcurrent":True}]),
                         dict(label='Pause', method='animate', args=[[None], {"frame": {"duration":0,"redraw":False}, "mode":"immediate"}])]
            )]
        ),
        frames=frames
    )

    # If Pydroid fails to render animation, export to HTML
    try:
        fig.show()
    except Exception as e:
        print("Animation not supported inline; exporting to HTML...")
        fig.write_html("/storage/emulated/0/plot3D.html")
        print("Open '/storage/emulated/0/plot3D.html' in browser to view animation.")

# ----------------------------
# Interactive controls
# ----------------------------
interact(interactive_3D,
         param_to_animate=Dropdown(options=['perturbation','limb_absorption','air_loss_factor'], value='perturbation', description='Animate'),
         param_min=FloatSlider(min=0.0, max=1.0, step=0.05, value=0.0, description='Min'),
         param_max=FloatSlider(min=0.1, max=1.0, step=0.05, value=1.0, description='Max'),
         frames_count=IntSlider(min=5, max=20, step=1, value=10, description='Frames'),
         limb_absorption=FloatSlider(min=0.0, max=0.9, step=0.05, value=0.5),
         air_loss_factor=FloatSlider(min=0.1, max=1.0, step=0.05, value=1.0))