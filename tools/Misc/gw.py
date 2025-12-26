import numpy as np

# ----- Parameters -----
N = 5  # atoms per side (5x5x5 lattice for phone)
mass = 1.0
E_b = 2.3  # eV, simple harmonic bond energy
r0 = 2.35  # Å, bond length
dt = 0.01  # time step
steps = 200  # small number of steps for phone

# ----- Initialize lattice positions -----
positions = np.zeros((N, N, N, 3))
velocities = np.zeros_like(positions)
forces = np.zeros_like(positions)

for i in range(N):
    for j in range(N):
        for k in range(N):
            positions[i,j,k] = np.array([i*r0, j*r0, k*r0])

# Introduce a pre-crack by removing a plane of atoms
precrack_layer = 0
positions[:, :, precrack_layer, :] = np.nan  # mark atoms as missing

# ----- Define nearest neighbors -----
neighbors = [np.array([1,0,0]), np.array([-1,0,0]),
             np.array([0,1,0]), np.array([0,-1,0]),
             np.array([0,0,1]), np.array([0,0,-1])]

# ----- Force calculation -----
def compute_forces(pos):
    F = np.zeros_like(pos)
    Nx, Ny, Nz, _ = pos.shape
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                if np.isnan(pos[i,j,k,0]):
                    continue  # skip missing atoms
                for nb in neighbors:
                    ni, nj, nk = i+nb[0], j+nb[1], k+nb[2]
                    if 0 <= ni < Nx and 0 <= nj < Ny and 0 <= nk < Nz:
                        if np.isnan(pos[ni,nj,nk,0]):
                            continue
                        r_vec = pos[ni,nj,nk] - pos[i,j,k]
                        r = np.linalg.norm(r_vec)
                        dr = r - r0
                        f = (2*E_b/r0) * dr * (r_vec/r)
                        F[i,j,k] += f
    return F

# ----- Integration loop (Velocity Verlet) -----
for step in range(steps):
    forces = compute_forces(positions)
    velocities += 0.5 * forces / mass * dt
    positions += velocities * dt
    forces_new = compute_forces(positions)
    velocities += 0.5 * forces_new / mass * dt

    # Check for bond breaking (stretch >1.5*r0)
    broken = 0
    Nx, Ny, Nz, _ = positions.shape
    for i in range(Nx):
        for j in range(Ny):
            for k in range(Nz):
                if np.isnan(positions[i,j,k,0]):
                    continue
                for nb in neighbors:
                    ni, nj, nk = i+nb[0], j+nb[1], k+nb[2]
                    if 0 <= ni < Nx and 0 <= nj < Ny and 0 <= nk < Nz:
                        if np.isnan(positions[ni,nj,nk,0]):
                            continue
                        r = np.linalg.norm(positions[ni,nj,nk] - positions[i,j,k])
                        if r > 1.5*r0:
                            broken += 1
    if step % 20 == 0:
        print(f"Step {step}, broken bonds: {broken}")


