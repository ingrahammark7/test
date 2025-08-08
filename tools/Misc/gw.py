# Python code to model hover stability for a Mavic-like quadcopter.
# This code will:
# - Simulate horizontal drift caused by an initial tilt (theta0) that the controller corrects after a latency.
# - The tilt decays exponentially after controller action with a time constant tau_c (combined controller+motor response).
# - Compute peak horizontal displacement during recovery and peak horizontal velocity.
# - Sweep theta0, latency, and tau_c and present results as plots and a table.
#
# NOTE: This runs in the notebook environment and uses matplotlib (no seaborn). It will display a plot and a table.
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from math import sin

# Parameters
g = 9.81  # gravity (m/s^2)
m = 0.9   # mass (kg) - representative Mavic-ish
# Simulation settings
theta0_deg = np.linspace(0.1, 30.0, 300)  # initial tilt angles in degrees (0.1° to 30°)
theta0 = np.deg2rad(theta0_deg)  # radians

latencies = [0.005, 0.02, 0.05, 0.1]   # controller latencies (s): 5ms, 20ms, 50ms, 100ms
tau_cs = [0.01, 0.02, 0.05, 0.1]      # recovery time constants (s): fast to slow (10ms-100ms)

# Function to compute horizontal displacement from tilt profile
# theta(t) = theta0 for t < latency
# theta(t) = theta0 * exp(-(t-latency)/tau_c) for t >= latency
# horizontal acceleration a(t) = g * sin(theta(t))
# integrate twice to get displacement (assume initial vel=0, pos=0)
def displacement_for_params(theta0_rad, latency, tau_c, tmax=1.0, dt=1e-4):
    # we'll integrate until tmax (enough to capture transient)
    t = np.arange(0, tmax, dt)
    theta = np.where(t < latency, theta0_rad, theta0_rad * np.exp(-(t - latency)/tau_c))
    a = g * np.sin(theta)  # horizontal acceleration
    v = np.cumsum(a) * dt
    x = np.cumsum(v) * dt
    # return peak displacement and final displacement and peak velocity
    return x.max(), x[-1], v.max()

# Sweep and collect results
rows = []
for latency in latencies:
    for tau_c in tau_cs:
        max_disps = []
        final_disps = []
        peak_vs = []
        for th in theta0:
            xpeak, xfinal, vpeak = displacement_for_params(th, latency, tau_c, tmax=1.0, dt=1e-4)
            max_disps.append(xpeak)
            final_disps.append(xfinal)
            peak_vs.append(vpeak)
        max_disps = np.array(max_disps)
        final_disps = np.array(final_disps)
        peak_vs = np.array(peak_vs)
        # Find allowable theta for thresholds (1 cm and 5 cm)
        thresh1 = 0.01  # 1 cm
        thresh5 = 0.05  # 5 cm
        def theta_for_thresh(th_arr, disp_arr, thresh):
            idx = np.where(disp_arr <= thresh)[0]
            if len(idx) == 0:
                return None
            return np.rad2deg(theta0[idx[-1]])  # largest theta that meets requirement
        theta1 = theta_for_thresh(theta0, max_disps, thresh1)
        theta5 = theta_for_thresh(theta0, max_disps, thresh5)
        # store summary row
        rows.append({
            "latency_s": latency,
            "tau_c_s": tau_c,
            "theta_allow_1cm_deg": theta1,
            "theta_allow_5cm_deg": theta5,
            "max_disp_at_5deg_m": float(max_disps[np.argmin(np.abs(theta0 - np.deg2rad(5.0)))]),
            "max_disp_at_10deg_m": float(max_disps[np.argmin(np.abs(theta0 - np.deg2rad(10.0)))]),
        })

df = pd.DataFrame(rows)

# Plot examples of tilt decay and displacement for a chosen scenario
example_latency = 0.02
example_tau = 0.02
example_theta_deg = [1.0, 2.0, 5.0, 10.0]  # degrees
t = np.arange(0, 0.5, 1e-4)
plt.figure(figsize=(8,4))
for thd in example_theta_deg:
    th = np.deg2rad(thd)
    theta_t = np.where(t < example_latency, th, th * np.exp(-(t - example_latency)/example_tau))
    a_t = g * np.sin(theta_t)
    v_t = np.cumsum(a_t) * (t[1]-t[0])
    x_t = np.cumsum(v_t) * (t[1]-t[0])
    plt.plot(t, x_t, label=f"{thd}° -> peak {x_t.max():.3f} m")
plt.xlabel("Time (s)")
plt.ylabel("Horizontal displacement (m)")
plt.title(f"Displacement vs time (latency={example_latency}s, tau_c={example_tau}s)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Display results table for summary thresholds
import caas_jupyter_tools as tools; tools.display_dataframe_to_user("Hover stability summary", df)

# Also print a small textual summary for convenience
print("Summary table displayed: shows allowable initial tilt (deg) for <=1 cm and <=5 cm max displacement\n")
print(df.to_string(index=False))

# Full runnable quadcopter simulator (Mavic-like) with:
# - 6-DOF rigid-body (small-angle simplifications for thrust direction)
# - Motor+prop 1st-order dynamics (omega response)
# - PID attitude (rate+angle cascade) and PD position controller
# - Simple complementary filter for attitude estimation (as placeholder EKF)
# - Wind gust model (filtered white noise)
# - Plots and a summary table
#
# Usage: run this cell; it will simulate and display time-series plots and a table.
# You can tweak parameters in the "CONFIG" section.
import numpy as np
import math
import matplotlib.pyplot as plt
import pandas as pd
from math import sin, cos
import time
# For interactive dataframe display in notebook UI
import caas_jupyter_tools as tools

# -------------------- CONFIG --------------------
SIM_TIME = 10.0        # seconds
DT = 0.001             # inner loop timestep (1 kHz)
STEPS = int(SIM_TIME / DT)

# Quadcopter physical params (Mavic-like)
m = 0.9                # kg
g = 9.81               # m/s^2
arm = 0.225            # m (distance from center to motor)
Ixx = 0.011            # kg*m^2
Iyy = 0.011
Izz = 0.02
I = np.diag([Ixx, Iyy, Izz])
I_inv = np.linalg.inv(I)

# Motor/prop params (first-order)
kT = 1.2e-5            # thrust coefficient (N/(rad/s)^2) -- tune so hover works
kQ = 2.0e-7            # torque coefficient (Nm/(rad/s)^2)
tau_m = 0.02           # motor time constant (s)

# Controller rates
ATT_RATE_HZ = 500     # inner rate loop frequency
POS_RATE_HZ = 50      # outer position loop frequency
ATT_RATE_STEP = int(1.0/ATT_RATE_HZ / DT)
POS_RATE_STEP = int(1.0/POS_RATE_HZ / DT)

# PID gains (tuned for this sim -- adjust for your own platform)
# Angle (outer) -> desired rates
Kp_ang = np.array([6.0, 6.0, 3.0])   # roll, pitch, yaw (deg->rad scaled effectively)
Kd_ang = np.array([0.3, 0.3, 0.1])

# Rate (inner) -> torque command
Kp_rate = np.array([0.12, 0.12, 0.06])
Kd_rate = np.array([0.002, 0.002, 0.001])

# Position PD
Kp_pos = np.array([1.2, 1.2, 6.0])
Kd_pos = np.array([0.8, 0.8, 3.0])

# Wind/gust model
gust_tau = 0.5   # seconds (lowpass)
gust_sigma = 1.0 # m/s (strength)

# Misc
hover_height = 0.0  # target z (relative)
thrust_limits = (0.0, 1.0)  # throttle fraction (0..1)

# -------------------- UTILITIES --------------------
def quat_from_euler(phi, theta, psi):
    # ZYX rotation (psi yaw, theta pitch, phi roll)
    c1 = math.cos(psi/2); s1 = math.sin(psi/2)
    c2 = math.cos(theta/2); s2 = math.sin(theta/2)
    c3 = math.cos(phi/2); s3 = math.sin(phi/2)
    qw = c1*c2*c3 + s1*s2*s3
    qx = c1*c2*s3 - s1*s2*c3
    qy = c1*s2*c3 + s1*c2*s3
    qz = s1*c2*c3 - c1*s2*s3
    return np.array([qw, qx, qy, qz])

def euler_from_quat(q):
    qw, qx, qy, qz = q
    # roll (x)
    sinr_cosp = 2*(qw*qx + qy*qz)
    cosr_cosp = 1 - 2*(qx*qx + qy*qy)
    roll = math.atan2(sinr_cosp, cosr_cosp)
    # pitch (y)
    sinp = 2*(qw*qy - qz*qx)
    if abs(sinp) >= 1:
        pitch = math.copysign(math.pi/2, sinp)
    else:
        pitch = math.asin(sinp)
    # yaw (z)
    siny_cosp = 2*(qw*qz + qx*qy)
    cosy_cosp = 1 - 2*(qy*qy + qz*qz)
    yaw = math.atan2(siny_cosp, cosy_cosp)
    return np.array([roll, pitch, yaw])

def quat_mult(q, r):
    # quaternion multiply q * r
    qw, qx, qy, qz = q
    rw, rx, ry, rz = r
    return np.array([
        qw*rw - qx*rx - qy*ry - qz*rz,
        qw*rx + qx*rw + qy*rz - qz*ry,
        qw*ry - qx*rz + qy*rw + qz*rx,
        qw*rz + qx*ry - qy*rx + qz*rw
    ])

def small_angle_rotate(acc_body, quat):
    # rotate body vector to inertial (approx using full quat)
    qw, qx, qy, qz = quat
    R = np.array([
        [1-2*(qy**2+qz**2), 2*(qx*qy - qz*qw), 2*(qx*qz + qy*qw)],
        [2*(qx*qy + qz*qw), 1-2*(qx**2+qz**2), 2*(qy*qz - qx*qw)],
        [2*(qx*qz - qy*qw), 2*(qy*qz + qx*qw), 1-2*(qx**2+qy**2)]
    ])
    return R @ acc_body, R

# -------------------- STATE & LOG ARRAYS --------------------
# state: position, velocity, quaternion, angular rates, motor rpms
p = np.array([0.0, 0.0, 0.0])     # inertial (x,y,z) (z up positive)
v = np.array([0.0, 0.0, 0.0])
quat = quat_from_euler(0.0, 0.0, 0.0)
omega = np.array([0.0, 0.0, 0.0])
motor_omega = np.zeros(4)         # rad/s

# desired setpoint (hover at origin)
p_des = np.array([0.0, 0.0, 0.0])
v_des = np.array([0.0, 0.0, 0.0])
euler_des = np.array([0.0, 0.0, 0.0])

# estimator (simple complementary filter for attitude)
est_euler = np.array([0.0, 0.0, 0.0])   # roll,pitch,yaw estimate
alpha_att = 0.995   # blending for gyro integration vs accel

# wind/gust state
gust_v = np.array([0.0, 0.0, 0.0])

# logs
log_t = np.zeros(STEPS)
log_p = np.zeros((STEPS,3))
log_v = np.zeros((STEPS,3))
log_euler = np.zeros((STEPS,3))
log_est_euler = np.zeros((STEPS,3))
log_motor = np.zeros((STEPS,4))
log_throttle = np.zeros((STEPS,4))

# small utility: mixer for quad-X (motor order: front-left, front-right, rear-right, rear-left)
# We'll use motor indices [0,1,2,3] in X configuration
def mixer_from_total(T_total, tau_phi, tau_theta, tau_psi):
    # Solve mixing matrix (from earlier description)
    # T1 T2 T3 T4  =>  rows: total thrust, tau_phi, tau_theta, tau_psi
    # For simplicity assume tau_psi is produced by alternating rotor torque with sign pattern [+ - + -]
    l = arm
    kM = kQ / kT  # not exact, but ratio for sign
    # Build linear system A * T = b
    A = np.array([
        [1, 1, 1, 1],
        [ l, -l, -l,  l],  # roll torque mapping (approx for X)
        [-l, -l,  l,  l],  # pitch torque mapping (approx for X)
        [ kM, -kM, kM, -kM]
    ])
    b = np.array([T_total, tau_phi, tau_theta, tau_psi])
    # Solve for T_i (allow negative temporarily then clip)
    Ti, *_ = np.linalg.lstsq(A, b, rcond=None)
    return Ti

# -------------------- SIM LOOP --------------------
np.random.seed(1)
start_time = time.time()
for k in range(STEPS):
    t = k * DT
    log_t[k] = t

    # ---- sensor/gust update ----
    # simple gust: filtered white-noise in horizontal plane
    w = np.random.randn(3) * gust_sigma * math.sqrt(DT)
    gust_v += (DT / gust_tau) * (-gust_v + w)  # first-order lowpass
    # total wind relative to inertial frame (assume only horizontal)
    wind_inertial = np.array([gust_v[0], gust_v[1], 0.0])

    # ---- estimator (attitude complementary filter using gyro+accel) ----
    # Simulate IMU (gyro perfect + small noise; accel measures gravity+body acc)
    gyro_meas = omega + np.random.randn(3) * 0.002  # rad/s noise
    # accel in body: compute actual accel_inertial (including gravity)
    # For estimator use only gravity direction (accelerometer) by assuming small translational accel
    # compute roll/pitch from accel (approx)
    # rotate gravity into body frame: g_body = R^T @ [0,0,g]
    _, Rmat = small_angle_rotate(np.zeros(3), quat)
    g_body = Rmat.T @ np.array([0,0,g])
    # accelerometer measurement direction (neg gravity)
    accel_meas_body = -g_body + np.random.randn(3) * 0.1  # m/s^2 noise

    # get roll/pitch from accel_meas (simple)
    acc_roll = math.atan2(accel_meas_body[1], accel_meas_body[2])
    acc_pitch = math.atan2(-accel_meas_body[0], math.sqrt(accel_meas_body[1]**2 + accel_meas_body[2]**2))
    # gyro integration for angles
    est_euler += gyro_meas * DT  # crude: omega =~ euler rates for small angles
    # blend with accel estimates (complementary)
    est_euler[0] = alpha_att * est_euler[0] + (1-alpha_att) * acc_roll
    est_euler[1] = alpha_att * est_euler[1] + (1-alpha_att) * acc_pitch
    # yaw left from gyro integration (no magnetometer here)

    # log estimator
    log_est_euler[k,:] = est_euler

    # ---- control (position outer loop slower) ----
    if (k % POS_RATE_STEP) == 0:
        # position error (z positive up, but we want to hold altitude at 0)
        e_pos = p_des - p
        e_vel = v_des - v
        a_des = Kp_pos * e_pos + Kd_pos * e_vel + np.array([0.0, 0.0, g])  # desired inertial accel (m/s^2)
        # Map desired accel to desired roll/pitch and thrust
        # For small angles: desired pitch = a_x/g; desired roll = -a_y/g
        phi_des = -a_des[1] / g
        theta_des = a_des[0] / g
        psi_des = 0.0
        euler_des = np.array([phi_des, theta_des, psi_des])
        # total thrust needed (approx): T_total = m * (a_des_z)
        # compute thrust (positive) as component along body z (approx with small angles)
        T_total = m * a_des[2]
        # limit to positive
        if T_total < 0.0:
            T_total = 0.0
    # ---- attitude controller (inner loop) ----
    if (k % ATT_RATE_STEP) == 0:
        # angle error (use estimator)
        ang_err = euler_des - est_euler
        # desired body rates from angle PD (approx)
        omega_des = Kp_ang * ang_err  # rad/s (works as proportional mapping)
        # rate error
        rate_err = omega_des - omega
        # torque command (Pd-like)
        tau_cmd = Kp_rate * rate_err - Kd_rate * omega  # simple derivative on measured rate
        # map torques + thrust to individual motor thrusts
        # Note: tau_cmd is desired body torques (roll, pitch, yaw)
        tau_phi, tau_theta, tau_psi = tau_cmd
        # convert total thrust (N) to per-motor thrusts via mixer
        T_cmds = mixer_from_total(T_total, tau_phi, tau_theta, tau_psi)
        # ensure non-negative and compute throttle fraction estimate
        # translate desired thrust to desired motor omega: T = kT * w^2 => w = sqrt(T/kT)
        omega_cmds = np.zeros(4)
        for i in range(4):
            Ti = max(0.0, T_cmds[i])
            omega_cmds[i] = math.sqrt(max(0.0, Ti / kT + 1e-12))
        # convert to throttle fraction (normalize by a chosen max omega)
        max_omega_possible = 900.0  # rad/s (tunable)
        throttle_cmds = np.clip(omega_cmds / max_omega_possible, thrust_limits[0], thrust_limits[1])
    # ---- motor dynamics: first-order response to throttle -> omega ----
    # simple mapping throttle -> commanded omega linear scaled
    for i in range(4):
        target = throttle_cmds[i] * max_omega_possible
        motor_omega[i] += (DT / tau_m) * (target - motor_omega[i])
        # compute thrust and torque produced by motor/prop
        # T = kT * w^2, torque = kQ * w^2
    thrusts = kT * motor_omega**2
    torques = kQ * motor_omega**2 * np.array([1.0, -1.0, 1.0, -1.0])  # rotor torque signs


    # ---- dynamics integration (rigid body) ----
    # total thrust force in body frame (z axis positive up in body)
    F_body = np.array([0.0, 0.0, np.sum(thrusts)])
    # rotate to inertial
    F_inertial, Rmat = small_angle_rotate(F_body, quat)
    # include gravity and simple drag and wind disturbance (wind acts as airspeed -> drag)
    # Compute drag as linear viscous for simplicity
    v_air = v - wind_inertial  # relative airspeed (inertial frame)
    c_drag = 0.5
    F_drag = -c_drag * v_air
    F_net = F_inertial + np.array([0.0,0.0,-m*g]) + F_drag
    a = F_net / m
    v += a * DT
    p += v * DT

    # rotational torques from thrust offsets and rotor reaction torques
    # roll torque ~ l*(T2 + T3 - T1 - T4) depending on mapping; we'll use approximate mapping
    tau_roll = arm * (thrusts[1] + thrusts[2] - thrusts[0] - thrusts[3])
    tau_pitch = arm * (-thrusts[0] - thrusts[1] + thrusts[2] + thrusts[3])
    tau_yaw = np.sum(torques)
    tau_total = np.array([tau_roll, tau_pitch, tau_yaw])
    # rotational dynamics
    omega_dot = I_inv @ (tau_total - np.cross(omega, I @ omega))
    omega += omega_dot * DT

    # integrate quaternion from omega
    # quaternion derivative: 0.5 * Omega(omega) * q
    qw, qx, qy, qz = quat
    ox, oy, oz = omega
    Omega = np.array([
        [0.0, -ox, -oy, -oz],
        [ox,  0.0,  oz, -oy],
        [oy, -oz,  0.0,  ox],
        [oz,  oy, -ox,  0.0]
    ])
    dq = 0.5 * Omega @ quat
    quat += dq * DT
    quat /= np.linalg.norm(quat)

    # log states
    log_p[k,:] = p
    log_v[k,:] = v
    log_euler[k,:] = euler_from_quat(quat)
    log_motor[k,:] = motor_omega
    log_throttle[k,:] = throttle_cmds

end_time = time.time()

# -------------------- POSTPROCESS & PLOTS --------------------
print(f"Simulation complete in {end_time-start_time:.2f} s (simulated {SIM_TIME:.1f} s, dt={DT}s).")

# Create dataframe summary at end
df_summary = pd.DataFrame({
    "time_s": log_t,
    "pos_x_m": log_p[:,0],
    "pos_y_m": log_p[:,1],
    "pos_z_m": log_p[:,2],
    "vel_x_m_s": log_v[:,0],
    "vel_y_m_s": log_v[:,1],
    "vel_z_m_s": log_v[:,2],
    "roll_rad": log_euler[:,0],
    "pitch_rad": log_euler[:,1],
    "yaw_rad": log_euler[:,2],
})
tools.display_dataframe_to_user("Simulation state time series (sample)", df_summary.head(200))

# Plot position and attitude
tvec = log_t
fig, axs = plt.subplots(3,1, figsize=(9,9), constrained_layout=True)
axs[0].plot(tvec, log_p[:,0]); axs[0].set_ylabel("x (m)"); axs[0].grid(True)
axs[1].plot(tvec, log_p[:,1]); axs[1].set_ylabel("y (m)"); axs[1].grid(True)
axs[2].plot(tvec, log_p[:,2]); axs[2].set_ylabel("z (m)"); axs[2].set_xlabel("time (s)"); axs[2].grid(True)
fig.suptitle("Position vs time")

fig2, axs2 = plt.subplots(3,1, figsize=(9,9), constrained_layout=True)
axs2[0].plot(tvec, log_euler[:,0]); axs2[0].set_ylabel("roll (rad)"); axs2[0].grid(True)
axs2[1].plot(tvec, log_euler[:,1]); axs2[1].set_ylabel("pitch (rad)"); axs2[1].grid(True)
axs2[2].plot(tvec, log_euler[:,2]); axs2[2].set_ylabel("yaw (rad)"); axs2[2].set_xlabel("time (s)"); axs2[2].grid(True)
fig2.suptitle("Attitude (Euler) vs time")

fig3, axs3 = plt.subplots(2,1, figsize=(9,6), constrained_layout=True)
axs3[0].plot(tvec, log_motor[:,0]); axs3[0].set_ylabel("motor omega[0] (rad/s)"); axs3[0].grid(True)
axs3[1].plot(tvec, log_throttle[:,0]); axs3[1].set_ylabel("throttle[0]"); axs3[1].set_xlabel("time (s)"); axs3[1].grid(True)
fig3.suptitle("Motor omega and throttle (motor 0 sample)")

plt.show()

# Print final state snapshot
final = {
    "final_pos_m": log_p[-1,:].tolist(),
    "final_vel_m_s": log_v[-1,:].tolist(),
    "final_euler_rad": log_euler[-1,:].tolist(),
    "final_motor_omega_rad_s": log_motor[-1,:].tolist()
}
print("Final state snapshot:")
print(final)