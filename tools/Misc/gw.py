import numpy as np
import plotly.graph_objects as go

# ----------------------------
# Depth and time parameters
# ----------------------------
depth = np.linspace(0, 0.6, 300)
time_steps = np.linspace(0, 1, 30)  # normalized time 0->1
layer_thicknesses = np.array([0.2, 0.5, 0.8])
standoffs = np.array([0.1, 0.2, 0.3])
materials = ["Steel", "Ceramic", "Gel"]
z_offsets = [i*50 for i in range(len(layer_thicknesses))]

# ----------------------------
# Compute energy deposition per layer
# ----------------------------
def compute_layer_wave(thickness, standoff, limb, perturb, air_loss, t):
    peak_depth = 0.15 + 0.3*t - 0.15 * perturb
    width = 0.10 + 0.05*np.clip((thickness-0.8)/0.5,0,1)
    amplitude = 500 * (1 - np.clip((thickness-0.8)/0.5,0,1))
    air_factor = 1 / (1 + (standoff/0.3)**2)
    curve = amplitude * np.exp(-((depth - peak_depth)/width)**2)
    curve *= air_factor * (1 - limb) * air_loss
    return curve

# ----------------------------
# Build frames for animation
# ----------------------------
def build_frames(limb, perturb, air_loss):
    frames = []
    for t in time_steps:
        frame_data = []
        for idx, thickness in enumerate(layer_thicknesses):
            for s in standoffs:
                curve = compute_layer_wave(thickness, s, limb, perturb, air_loss, t)
                z_offset = z_offsets[idx]
                # layer curve
                frame_data.append(go.Scatter3d(
                    x=depth,
                    y=[thickness]*len(depth),
                    z=curve+z_offset,
                    mode='lines',
                    line=dict(width=2),
                    showlegend=False
                ))
                # dynamic peak marker
                max_val = curve.max()
                peak_depth = depth[np.argmax(curve)]
                frame_data.append(go.Scatter3d(
                    x=[peak_depth],
                    y=[thickness],
                    z=[max_val+z_offset],
                    mode='markers+text',
                    marker=dict(color='red', size=5),
                    text=[f"{max_val:.1f} J/m"],
                    textposition="top center",
                    showlegend=False
                ))
        frames.append(go.Frame(data=frame_data, name=str(round(t,2))))
    return frames

# ----------------------------
# Initial parameters
# ----------------------------
limb_values = np.linspace(0,0.8,3)
perturb_values = np.linspace(0,1,3)
air_values = np.linspace(0.5,1.5,3)
initial_limb = limb_values[0]
initial_perturb = perturb_values[0]
initial_air = air_values[0]

# ----------------------------
# Build initial figure
# ----------------------------
frames = build_frames(initial_limb, initial_perturb, initial_air)
fig = go.Figure(data=frames[0].data, frames=frames)

# ----------------------------
# Slider steps for parameter presets
# ----------------------------
slider_steps = []
for limb in limb_values:
    for perturb in perturb_values:
        for air_loss in air_values:
            new_frames = build_frames(limb, perturb, air_loss)
            step = dict(
                method="animate",
                args=[[f.name for f in new_frames],
                      {"frame":{"duration":50,"redraw":True}, "mode":"immediate"}],
                label=f"L:{limb:.2f} P:{perturb:.2f} A:{air_loss:.2f}"
            )
            slider_steps.append(step)

sliders = [dict(active=0, pad={"t":50}, steps=slider_steps)]

# ----------------------------
# Layout and buttons
# ----------------------------
fig.update_layout(
    sliders=sliders,
    updatemenus=[dict(
        type="buttons",
        showactive=False,
        buttons=[dict(label="Play",
                      method="animate",
                      args=[None, {"frame":{"duration":100,"redraw":True}, "fromcurrent":True}]),
                 dict(label="Pause",
                      method="animate",
                      args=[[None], {"frame":{"duration":0,"redraw":False}, "mode":"immediate"}])]
    )],
    title="Pydroid3-Compatible Multi-Layer Wave Dashboard",
    scene=dict(
        xaxis_title='Depth (m)',
        yaxis_title='Layer Thickness (HVL)',
        zaxis_title='Energy (J/m)'
    ),
    height=700
)

# ----------------------------
# Show figure
# ----------------------------
fig.show()