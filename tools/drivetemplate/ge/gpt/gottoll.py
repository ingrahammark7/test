import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import TextBox

# Constants in CGS units
g = 980  # gravitational acceleration in cm/s^2
m = 1000  # mass of the ball in grams (1 kg)
initial_energy = 1e7  # initial kinetic energy in ergs (100 J = 10^7 ergs)
time_step = 0.01  # time step in seconds (CGS)
elastic_collisions = 0  # sum of all energy exchanges during collisions

# Initial velocity from kinetic energy
v0 = np.sqrt(2 * initial_energy / m)  # in cm/s

# Function to calculate total energy
def total_energy(v, h, stopping_energy):
    kinetic_energy = 0.5 * m * v**2  # Kinetic energy in ergs
    potential_energy = m * g * h  # Potential energy in ergs
    return kinetic_energy + potential_energy + stopping_energy

# Stopping height configuration (a significant part of the maximum height)
stopped_height_fraction = 0.5  # Fraction of max height where the ball is stopped
max_height = (v0**2) / (2 * g)  # Maximum height in cm (derived from kinematics)
stopped_height = stopped_height_fraction * max_height  # Stopping height in cm

# Initial setup
height = 0  # initial height in cm
velocity = v0  # initial upward velocity in cm/s
t = 0  # time in seconds
force_energy = 0  # placeholder for energy to stop the ball

# Arrays for visualization
heights = []
energies = []

# Simulate upward and downward motion
stopping_energy = 0  # potential stopping energy (to be used later)
while True:
    # Update position and velocity
    height += velocity * time_step
    velocity -= g * time_step  # gravity effect

    # Calculate stopping energy once reaching the stopping height
    if height <= stopped_height and velocity < 0:
        stopping_energy = 0.5 * m * velocity**2  # Calculate stopping force energy
        velocity = 0  # stop velocity
        break

    # Store data
    heights.append(height)
    energies.append(total_energy(velocity, height, stopping_energy))

# After stopping, allow the ball to fall back to the ground
while height > 0:
    velocity += g * time_step  # gravity effect
    height -= velocity * time_step  # update position

    # Store data
    heights.append(height)
    energies.append(total_energy(velocity, height, stopping_energy))

    # Check for ground collision
    if height <= 0:
        height = 0
        velocity = -velocity  # elastic collision (reverse velocity)
        elastic_collisions += 0.5 * m * velocity**2  # energy exchanged
        break

# Total energy verification
final_energy = total_energy(velocity, height, 0)  # Stopping energy is used

# Text Output Box Content
text_output = f"""
Initial Energy (Launch + Stopping Force): {initial_energy + stopping_energy:.2e} ergs
Stopping Height: {stopped_height:.2f} cm
Stopping Energy: {stopping_energy:.2e} ergs
Elastic Collision Energy Exchange: {elastic_collisions:.2e} ergs
Final Energy: {final_energy:.2e} ergs
Total Energy Conserved (Initial - Final): {initial_energy + stopping_energy - final_energy:.2e} ergs
"""

# Visualization
fig, ax = plt.subplots(figsize=(10, 6))
plt.subplots_adjust(bottom=0.4)  # Adjust to leave space for the text box

# Plot height and energy
ax.plot(heights, label="Height (cm)")
ax.plot(energies, label="Total Energy (ergs)")
ax.set_xlabel("Time Steps")
ax.set_ylabel("Values")
ax.set_title("Height and Energy Over Time")
ax.legend()
ax.grid()

# Text box display
text_box_ax = plt.axes([0.1, 0.05, 0.8, 0.3])  # Position: [x, y, width, height]
text_box = TextBox(text_box_ax, "", initial=text_output)
text_box_ax.set_facecolor('lightgray')
text_box_ax.get_children()[0].set_fontsize(10)  # Adjust font size
text_box_ax.get_children()[0].set_verticalalignment('top')  # Align text

plt.show()
