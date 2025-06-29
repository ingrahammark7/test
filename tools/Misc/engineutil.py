import math

# Baseline engine data: GE F100 turbofan (typical low bypass military turbofan)
BASELINE_ENGINE = {
    "name": "GE F100",
    "fan_diameter_m": 0.97,
    "bypass_ratio": 0.3,
    "fan_blade_count": 23,
    "blade_length_percent_radius": 0.62,  # fraction of radius
    "blade_width_percent_diameter": 0.05,  # fraction of diameter
    "thrust_lbf": 29000,
    "thrust_newton": 129000,
    "low_pressure_compressor_stages": 3,
    "high_pressure_compressor_stages": 10,
    "compressor_pressure_ratio": 23.5,  # overall (LPC * HPC)
    "turbine_inlet_temperature_K": 1680,
    "engine_length_m": 3.0,
    "engine_mass_kg": 1500,
    "specific_fuel_consumption_lb_per_lbf_hr": 0.78,
}

def scale_blade_count(fan_diameter_m, bypass_ratio,
                      baseline=BASELINE_ENGINE):
    """Estimate blade count scaling with fan diameter and bypass ratio."""
    bd = baseline["fan_diameter_m"]
    br = baseline["bypass_ratio"]
    bbc = baseline["fan_blade_count"]
    diameter_exp = 0.6
    bypass_exp = -0.3
    scale_factor = ((fan_diameter_m / bd) ** diameter_exp) * ((bypass_ratio / br) ** bypass_exp)
    blade_count = bbc * scale_factor
    return max(3, int(round(blade_count)))

def blade_length_percent_radius(bypass_ratio, baseline=BASELINE_ENGINE):
    """Estimate blade length as fraction of radius based on bypass ratio."""
    br_base = baseline["bypass_ratio"]
    length_base = baseline["blade_length_percent_radius"]
    length = length_base * (br_base / bypass_ratio)
    return max(0.3, min(0.9, length))

def blade_width_percent_diameter(fan_diameter_m, blade_count, baseline=BASELINE_ENGINE):
    """Estimate blade width as fraction of fan diameter."""
    circumference = math.pi * fan_diameter_m
    total_coverage = 0.7 * circumference  # blades cover ~70% circumference
    blade_width_m = total_coverage / blade_count
    width_percent = blade_width_m / fan_diameter_m
    return width_percent

def estimate_compressor_stages(thrust_newton, baseline=BASELINE_ENGINE):
    """
    Estimate LPC and HPC stages based on thrust scaling.
    Assume LPC scales slowly with thrust, HPC scales faster.
    """
    base_thrust = baseline["thrust_newton"]
    lpc_base = baseline["low_pressure_compressor_stages"]
    hpc_base = baseline["high_pressure_compressor_stages"]

    # LPC stages scale ~ (thrust)^0.15 (slow increase)
    lpc_stages = max(2, round(lpc_base * (thrust_newton / base_thrust) ** 0.15))
    # HPC stages scale ~ (thrust)^0.25
    hpc_stages = max(8, round(hpc_base * (thrust_newton / base_thrust) ** 0.25))

    return lpc_stages, hpc_stages

def estimate_compressor_pressure_ratio(lpc_stages, hpc_stages,
                                       baseline=BASELINE_ENGINE):
    """
    Estimate compressor pressure ratio based on total stages.
    Approximate exponential growth per stage.
    """
    base_lpc = baseline["low_pressure_compressor_stages"]
    base_hpc = baseline["high_pressure_compressor_stages"]
    base_cpr = baseline["compressor_pressure_ratio"]

    # Assume CPR scales exponentially with total stages
    total_stages = lpc_stages + hpc_stages
    base_stages = base_lpc + base_hpc
    cpr = base_cpr * (1.12 ** (total_stages - base_stages))
    return cpr

def estimate_turbine_inlet_temperature(thrust_newton, baseline=BASELINE_ENGINE):
    """
    Estimate turbine inlet temperature based on thrust.
    Higher thrust engines tend to run hotter but limited by materials.
    """
    base_tit = baseline["turbine_inlet_temperature_K"]
    base_thrust = baseline["thrust_newton"]
    tit = base_tit * (thrust_newton / base_thrust) ** 0.05
    return min(tit, 1800)  # cap near modern material limits

def estimate_engine_mass(thrust_newton, fan_diameter_m, baseline=BASELINE_ENGINE):
    """
    Estimate engine mass scaling with thrust and diameter.
    Mass roughly scales linearly with thrust and some allometric scaling with diameter.
    """
    base_mass = baseline["engine_mass_kg"]
    base_thrust = baseline["thrust_newton"]
    base_diameter = baseline["fan_diameter_m"]

    mass = base_mass * (thrust_newton / base_thrust) * (fan_diameter_m / base_diameter) ** 0.7
    return mass

def estimate_engine_length(fan_diameter_m, thrust_newton, baseline=BASELINE_ENGINE):
    """
    Estimate engine length scaling roughly with diameter and thrust.
    """
    base_length = baseline["engine_length_m"]
    base_thrust = baseline["thrust_newton"]
    base_diameter = baseline["fan_diameter_m"]

    length = base_length * (fan_diameter_m / base_diameter) ** 0.8 * (thrust_newton / base_thrust) ** 0.15
    return length

def estimate_core_diameter(fan_diameter_m, bypass_ratio):
    """
    Estimate core diameter from fan diameter and bypass ratio.
    Core flow = total flow / (1 + bypass), assume area scales with core diameter^2.
    """
    # Simplified: core diameter proportional to fan diameter / sqrt(1 + bypass)
    core_diameter = fan_diameter_m / math.sqrt(1 + bypass_ratio)
    return core_diameter

def estimate_specific_fuel_consumption(thrust_newton, baseline=BASELINE_ENGINE):
    """
    Rough estimate of SFC (lb/lbf/hr) decreasing with thrust.
    More thrust typically slightly better SFC but depends on engine type.
    """
    base_sfc = baseline["specific_fuel_consumption_lb_per_lbf_hr"]
    base_thrust = baseline["thrust_newton"]
    sfc = base_sfc * (base_thrust / thrust_newton) ** 0.1
    return sfc

def thrust_lbf_to_newton(thrust_lbf):
    return thrust_lbf * 4.44822

def thrust_newton_to_lbf(thrust_newton):
    return thrust_newton / 4.44822

def kelvin_to_celsius(k):
    return k - 273.15

def celsius_to_kelvin(c):
    return c + 273.15

def example_usage():
    new_fan_d = 1.2
    new_bypass = 0.8
    new_thrust_lbf = 40000
    new_thrust_N = thrust_lbf_to_newton(new_thrust_lbf)

    blade_ct = scale_blade_count(new_fan_d, new_bypass)
    blade_len_pct = blade_length_percent_radius(new_bypass)
    blade_w_pct = blade_width_percent_diameter(new_fan_d, blade_ct)
    lpc_stages, hpc_stages = estimate_compressor_stages(new_thrust_N)
    cpr = estimate_compressor_pressure_ratio(lpc_stages, hpc_stages)
    tit = estimate_turbine_inlet_temperature(new_thrust_N)
    mass = estimate_engine_mass(new_thrust_N, new_fan_d)
    length = estimate_engine_length(new_fan_d, new_thrust_N)
    core_d = estimate_core_diameter(new_fan_d, new_bypass)
    sfc = estimate_specific_fuel_consumption(new_thrust_N)

    print(f"Scaled Engine for Fan Diameter {new_fan_d} m, Bypass {new_bypass}, Thrust {new_thrust_lbf} lbf:")
    print(f"  Blade Count: {blade_ct}")
    print(f"  Blade Length % Radius: {blade_len_pct:.3f}")
    print(f"  Blade Width % Diameter: {blade_w_pct:.3f}")
    print(f"  LPC Stages: {lpc_stages}, HPC Stages: {hpc_stages}")
    print(f"  Compressor Pressure Ratio: {cpr:.2f}")
    print(f"  Turbine Inlet Temperature: {kelvin_to_celsius(tit):.1f} °C")
    print(f"  Estimated Engine Mass: {mass:.1f} kg")
    print(f"  Estimated Engine Length: {length:.2f} m")
    print(f"  Estimated Core Diameter: {core_d:.2f} m")
    print(f"  Estimated Specific Fuel Consumption: {sfc:.3f} lb/lbf/hr")

if __name__ == "__main__":
    example_usage()