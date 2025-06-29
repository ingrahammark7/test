import math

# Baseline engine data: GE F100 turbofan
BASELINE_ENGINE = {
    "name": "GE F100",
    "fan_diameter_m": 0.97,
    "bypass_ratio": 0.3,
    "fan_blade_count": 23,
    "blade_length_percent_radius": 0.62,  # example from literature/estimate
    "blade_width_percent_diameter": 0.05,  # approx 5% of fan diameter
    "thrust_lbf": 29000,
    "thrust_newton": 129000,
}

def scale_blade_count(fan_diameter_m, bypass_ratio,
                      baseline=BASELINE_ENGINE):
    """
    Estimate blade count scaling with fan diameter and bypass ratio.

    Empirically, blade count scales roughly with fan diameter^0.6 and inversely
    with bypass ratio^0.3, as higher bypass tend to have fewer blades.

    Parameters:
        fan_diameter_m: float, new fan diameter in meters
        bypass_ratio: float, new bypass ratio
        baseline: dict, baseline engine parameters

    Returns:
        int, estimated blade count (rounded)
    """
    bd = baseline["fan_diameter_m"]
    br = baseline["bypass_ratio"]
    bbc = baseline["fan_blade_count"]

    # Scaling exponents chosen to fit typical engine trends (tunable)
    diameter_exp = 0.6
    bypass_exp = -0.3

    scale_factor = ((fan_diameter_m / bd) ** diameter_exp) * ((bypass_ratio / br) ** bypass_exp)
    blade_count = bbc * scale_factor

    return max(3, int(round(blade_count)))  # minimum 3 blades for stability

def blade_length_percent_radius(bypass_ratio, baseline=BASELINE_ENGINE):
    """
    Estimate blade length as percentage of engine radius based on bypass ratio.

    Assumes an approximate linear inverse relation:
    higher bypass -> shorter blade length percent radius.

    Returns a float between 0 and 1.

    Parameters:
        bypass_ratio: float, engine bypass ratio
        baseline: dict, baseline engine parameters

    Returns:
        float, blade length as fraction of radius (0-1)
    """
    br_base = baseline["bypass_ratio"]
    length_base = baseline["blade_length_percent_radius"]

    # Simple linear inverse relation with 10% tolerance
    length = length_base * (br_base / bypass_ratio)
    length = max(0.3, min(0.9, length))  # clamp reasonable bounds

    return length

def blade_width_percent_diameter(fan_diameter_m, blade_count, baseline=BASELINE_ENGINE):
    """
    Estimate blade width as percent of fan diameter.

    Assumes total arc coverage ~70% of circumference divided by blade count,
    with some packing efficiency.

    Parameters:
        fan_diameter_m: float, fan diameter in meters
        blade_count: int, number of blades

    Returns:
        float, blade width as fraction of diameter
    """
    circumference = math.pi * fan_diameter_m
    total_coverage = 0.7 * circumference  # assume blades cover 70% of circumference
    blade_width_m = total_coverage / blade_count

    width_percent = blade_width_m / fan_diameter_m
    return width_percent

def thrust_lbf_to_newton(thrust_lbf):
    """Convert thrust from pounds-force to newtons."""
    return thrust_lbf * 4.44822

def thrust_newton_to_lbf(thrust_newton):
    """Convert thrust from newtons to pounds-force."""
    return thrust_newton / 4.44822

def scale_thrust(thrust_newton, scale_factor):
    """Scale thrust linearly by scale_factor."""
    return thrust_newton * scale_factor

def example_usage():
    # Example: scale an engine to fan diameter 1.2 m and bypass 0.8
    new_fan_d = 1.2
    new_bypass = 0.8

    blade_ct = scale_blade_count(new_fan_d, new_bypass)
    blade_len_pct = blade_length_percent_radius(new_bypass)
    blade_w_pct = blade_width_percent_diameter(new_fan_d, blade_ct)

    print(f"Scaled engine parameters for fan diameter={new_fan_d} m, bypass={new_bypass}:")
    print(f"  Blade count estimate: {blade_ct}")
    print(f"  Blade length (% radius): {blade_len_pct:.3f}")
    print(f"  Blade width (% diameter): {blade_w_pct:.3f}")

if __name__ == "__main__":
    example_usage()