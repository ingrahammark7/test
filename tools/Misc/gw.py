import math

def estimate_max_speed(
    rho_air,
    t_flight,
    T_ambient,
    T_max,
    C_h,
    rho_mat,
    c_mat,
    thickness,
    v_guess_low=100,
    v_guess_high=2000,
    tol=1e-2,
    max_iter=100
):
    def delta_T(v):
        q = C_h * (rho_air ** 0.5) * (v ** 3)
        heat_capacity_area = rho_mat * c_mat * thickness
        return q * t_flight / heat_capacity_area

    low, high = v_guess_low, v_guess_high
    for _ in range(max_iter):
        mid = (low + high) / 2
        T_surface = T_ambient + delta_T(mid)
        if abs(T_surface - T_max) < 0.1:
            return mid
        if T_surface > T_max:
            high = mid
        else:
            low = mid
        if high - low < tol:
            break
    return (low + high) / 2

def missile_range_with_speed_limit(
    m0, mp, thrust, burn_time, Cd, A, speed_limit, rho=1.225, v0=0
):
    mdot = mp / burn_time
    m1 = m0 - mp
    dt = 0.05  # timestep
    t = 0
    v = v0
    x = 0
    m = m0

    max_burn_iter = int(burn_time / dt) + 10
    for _ in range(max_burn_iter):
        if t >= burn_time:
            break
        drag = 0.5 * rho * Cd * A * v ** 2
        a = (thrust - drag) / m
        v_new = v + a * dt
        if v_new > speed_limit:
            v_new = speed_limit
            a = 0
        v = v_new
        x += v * dt
        m -= mdot * dt
        t += dt

    max_coast_iter = 2000
    for _ in range(max_coast_iter):
        if v <= 0:
            break
        drag = 0.5 * rho * Cd * A * v ** 2
        a = -drag / m1
        v_new = v + a * dt
        if v_new < 0:
            v_new = 0
        if abs(v_new - v) < 1e-4:
            break
        v = v_new
        x += v * dt

    return x

def air_density(altitude_m):
    # Simplified barometric formula for troposphere (up to ~11 km)
    if altitude_m < 11000:
        T0 = 288.15  # sea level temp K
        P0 = 101325  # sea level pressure Pa
        L = 0.0065    # lapse rate K/m
        R = 8.31447   # gas constant J/(mol·K)
        M = 0.0289644 # molar mass air kg/mol
        g = 9.80665   # gravity m/s^2

        T = T0 - L * altitude_m
        P = P0 * (T / T0) ** (g * M / (R * L))
        rho = P * M / (R * T)
        return rho
    else:
        return 0.15  # approximate for stratosphere

def run_varied_scenarios():
    T_ambient_sea_level = 288

    scenarios = {
        "R-23 Apex sea level": {
            "altitude": 0,
            "m0": 222,
            "mp": 140,
            "thrust": 5000,
            "burn_time": 6,
            "Cd": 0.5,
            "A": 0.025,
            "v0": 250,
            "T_max": 600,
            "rho_mat": 1900,
            "c_mat": 900,
            "thickness": 0.005,
            "C_h": 1.5e-4,
            "jam_effective": False,
        },
        "AIM-7 Sparrow medium altitude": {
            "altitude": 10000,
            "m0": 190,
            "mp": 110,
            "thrust": 4000,
            "burn_time": 5,
            "Cd": 0.45,
            "A": 0.02,
            "v0": 250,
            "T_max": 450,
            "rho_mat": 2200,
            "c_mat": 1400,
            "thickness": 0.002,
            "C_h": 1.5e-4,
            "jam_effective": True,
        },
        "AMRAAM AIM-120 high altitude": {
            "altitude": 15000,
            "m0": 150,
            "mp": 85,
            "thrust": 3500,
            "burn_time": 5,
            "Cd": 0.40,
            "A": 0.018,
            "v0": 250,
            "T_max": 350,
            "rho_mat": 1800,
            "c_mat": 1200,
            "thickness": 0.0015,
            "C_h": 1.5e-4,
            "jam_effective": True,
        },
        "AMRAAM AIM-120 multi-stage low altitude": {
            "altitude": 0,
            "m0": 150,
            "mp": 85 * 1.8,
            "thrust": 3500,
            "burn_time": 5 * 1.8,
            "Cd": 0.40,
            "A": 0.018,
            "v0": 250,
            "T_max": 350,
            "rho_mat": 1800,
            "c_mat": 1200,
            "thickness": 0.0015,
            "C_h": 1.5e-4,
            "jam_effective": True,
        },
    }

    for name, params in scenarios.items():
        altitude = params["altitude"]
        rho_air = air_density(altitude)
        T_ambient = T_ambient_sea_level - 0.0065 * altitude  # temp lapse approx
        t_flight_est = params["burn_time"] * 2

        max_speed = estimate_max_speed(
            rho_air=rho_air,
            t_flight=t_flight_est,
            T_ambient=T_ambient,
            T_max=params["T_max"],
            C_h=params["C_h"],
            rho_mat=params["rho_mat"],
            c_mat=params["c_mat"],
            thickness=params["thickness"],
            v_guess_high=2000,
        )

        range_m = missile_range_with_speed_limit(
            m0=params["m0"],
            mp=params["mp"],
            thrust=params["thrust"],
            burn_time=params["burn_time"],
            Cd=params["Cd"],
            A=params["A"],
            speed_limit=max_speed,
            rho=rho_air,
            v0=params["v0"],
        )

        jam_status = "Effective" if params["jam_effective"] else "Jammed (no function)"
        print(f"{name} @ {altitude} m:")
        print(f"  Air density = {rho_air:.3f} kg/m³")
        print(f"  Max radome-limited speed = {max_speed:.1f} m/s ({max_speed*3.6:.1f} km/h)")
        print(f"  Estimated max range = {range_m:.1f} m ({range_m/1000:.2f} km)")
        print(f"  Jamming status: {jam_status}\n")

if __name__ == "__main__":
    run_varied_scenarios()