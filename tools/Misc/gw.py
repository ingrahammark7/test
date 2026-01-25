import math

def optimal_bin_size(
    field_area_acres: float,
    yield_bushels_per_acre: float = 180,
    bulk_density_kg_per_m3: float = 750,
    max_bin_height_m: float = 3.0,
    shape: str = "square"
):
    """
    Compute optimal bin size to store all grain from a field.

    Parameters:
    - field_area_acres: area of the field in acres
    - yield_bushels_per_acre: corn yield (bushels per acre)
    - bulk_density_kg_per_m3: bulk density of corn grain
    - max_bin_height_m: practical maximum bin height (m)
    - shape: "square" or "circular" footprint

    Returns:
    - dictionary with optimal bin volume, footprint, dimensions, and land-use ratio
    """

    # Constants
    kg_per_ton = 1000
    m2_per_acre = 4046.8564224
    kg_per_bushel = 25.4

    # Convert yield to kg
    yield_kg_per_acre = yield_bushels_per_acre * kg_per_bushel

    # Total grain mass
    total_mass_kg = yield_kg_per_acre * field_area_acres
    total_mass_tons = total_mass_kg / kg_per_ton

    # Bin volume
    bin_volume_m3 = total_mass_kg / bulk_density_kg_per_m3

    # Bin footprint area
    bin_footprint_m2 = bin_volume_m3 / max_bin_height_m
    bin_footprint_acres = bin_footprint_m2 / m2_per_acre

    # Dimensions
    if shape == "square":
        side_m = math.sqrt(bin_footprint_m2)
        dimensions = {
            "side_m": side_m,
            "height_m": max_bin_height_m
        }
    elif shape == "circular":
        radius_m = math.sqrt(bin_footprint_m2 / math.pi)
        dimensions = {
            "radius_m": radius_m,
            "height_m": max_bin_height_m
        }
    else:
        dimensions = {"height_m": max_bin_height_m}

    # Land-use ratio (fraction of field area taken up)
    land_use_ratio = bin_footprint_acres / field_area_acres

    return {
        "field_area_acres": field_area_acres,
        "yield_bushels_per_acre": yield_bushels_per_acre,
        "total_mass_tons": total_mass_tons,
        "bin_volume_m3": bin_volume_m3,
        "bin_footprint_m2": bin_footprint_m2,
        "bin_footprint_acres": bin_footprint_acres,
        "land_use_ratio": land_use_ratio,
        "dimensions": dimensions
    }

# Example usage
if __name__ == "__main__":
    result = optimal_bin_size(field_area_acres=1.0, yield_bushels_per_acre=180, max_bin_height_m=3.0)
    print("Optimal Bin Result for 1 Acre:")
    for k, v in result.items():
        print(f"{k}: {v}")