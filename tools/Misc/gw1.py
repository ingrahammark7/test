import math
import json
import os
from typing import List

# -------------------------
# Material database
# -------------------------
materials = {
    "steel": {"density": 7850, "yield_strength": 1e9, "hardness": 500e6, "spall_factor": 0.8},
    "tungsten": {"density": 19250, "yield_strength": 1.5e9, "hardness": 700e6, "spall_factor": 0.7},
    "depleted_uranium": {"density": 19050, "yield_strength": 0.75e9, "hardness": 600e6, "spall_factor": 0.65},
    "ceramic": {"density": 3800, "yield_strength": 5e9, "hardness": 4e9, "spall_factor": 0.5}
}

# -------------------------
# Classes
# -------------------------
class ProjectileFragment:
    def __init__(self, mass, length, diameter, velocity, tip_type="pointed"):
        self.mass = mass
        self.length = length
        self.diameter = diameter
        self.velocity = velocity
        self.tip_type = tip_type
        self.remaining_length = length
        self.area = math.pi * (diameter/2)**2
        self.rod_ratio = length/diameter
        self.density = None

class Projectile:
    def __init__(self, name, material, mass, length, diameter, velocity, tip_type="pointed"):
        self.name = name
        self.material = material
        self.mass = mass
        self.length = length
        self.diameter = diameter
        self.velocity = velocity
        self.tip_type = tip_type
        self.fragments: List[ProjectileFragment] = []
        self.create_initial_fragment()

    def create_initial_fragment(self):
        frag = ProjectileFragment(self.mass, self.length, self.diameter, self.velocity, self.tip_type)
        frag.density = materials[self.material]["density"]
        self.fragments.append(frag)

class ArmorBlock:
    def __init__(self, material, thickness, angle=0):
        self.material = material
        self.thickness = thickness
        self.angle = angle
        self.density = materials[material]["density"]
        self.yield_strength = materials[material]["yield_strength"]
        self.hardness = materials[material]["hardness"]
        self.spall_factor = materials[material]["spall_factor"]

class ArmorLayer:
    def __init__(self, blocks: List[ArmorBlock]):
        self.blocks = blocks
        self.total_thickness = sum(block.thickness for block in blocks)

class ArmorPlate:
    def __init__(self, layers: List[ArmorLayer]):
        self.layers = layers
        self.total_thickness = sum(layer.total_thickness for layer in layers)

class PenetrationSimulation:
    def __init__(self, projectile: Projectile, armor_plate: ArmorPlate,
                 block_size=0.01, log_file="penetration_log.json"):
        self.projectile = projectile
        self.armor_plate = armor_plate
        self.block_size = block_size
        self.log_file = log_file
        self.penetration_total = 0.0
        self.log_data = []

    def run(self):
        for frag_index, fragment in enumerate(self.projectile.fragments):
            for layer_index, layer in enumerate(self.armor_plate.layers):
                for block_index, block in enumerate(layer.blocks):
                    n_subblocks = max(1, int(block.thickness / self.block_size))
                    subblock_thickness = block.thickness / n_subblocks

                    for sub_index in range(n_subblocks):
                        if fragment.remaining_length <= 0 or fragment.velocity <= 0:
                            break

                        KE = 0.5 * fragment.mass * fragment.velocity**2
                        P = KE / (fragment.area * block.yield_strength)
                        P *= (fragment.density / block.density) * (0.9 + 0.1 * fragment.rod_ratio)
                        P *= math.cos(math.radians(block.angle))

                        # Tip factor
                        tip_factor = 1.0
                        if fragment.tip_type == "pointed":
                            tip_factor = 1.1
                        elif fragment.tip_type == "blunt":
                            tip_factor = 0.9
                        P *= tip_factor

                        # Spall
                        P *= block.spall_factor
                        # Hardness correction
                        P *= (block.yield_strength / block.hardness)**0.25

                        # Obliquity dependent spall
                        P *= math.cos(math.radians(block.angle))

                        # Limit to block thickness
                        actual_pen = min(P, subblock_thickness)
                        self.penetration_total += actual_pen

                        # Energy absorption
                        energy_absorbed = KE * (actual_pen / P) if P > 0 else 0
                        fragment.velocity = math.sqrt(max(0, 2*(KE - energy_absorbed)/fragment.mass))

                        # Rod erosion
                        erosion_factor = 0.05
                        rod_erosion = erosion_factor * subblock_thickness
                        fragment.remaining_length = max(0, fragment.remaining_length - rod_erosion)

                        # Rod bending
                        bending_factor = 1.0 - 0.01*(sub_index / n_subblocks)
                        actual_pen *= bending_factor

                        # Projectile fragmentation (simplified)
                        if fragment.velocity > 3000 and fragment.remaining_length > 0.2:
                            new_mass = fragment.mass * 0.5
                            new_length = fragment.remaining_length * 0.5
                            new_diam = fragment.diameter
                            new_frag = ProjectileFragment(new_mass, new_length, new_diam, fragment.velocity, fragment.tip_type)
                            new_frag.density = fragment.density
                            self.projectile.fragments.append(new_frag)
                            fragment.mass *= 0.5
                            fragment.length *= 0.5

                        # Logging
                        log_entry = {
                            "fragment_index": frag_index+1,
                            "layer_index": layer_index+1,
                            "block_index": block_index+1,
                            "subblock_index": sub_index+1,
                            "material": block.material,
                            "penetration": round(actual_pen,5),
                            "remaining_velocity": round(fragment.velocity,2),
                            "remaining_rod_length": round(fragment.remaining_length,3),
                            "KE": round(KE,2)
                        }
                        self.log_data.append(log_entry)

        self.save_log()
        self.report()

    def save_log(self):
        with open(self.log_file, "w") as f:
            json.dump(self.log_data, f, indent=2)

    def report(self):
        print(f"Total penetration: {self.penetration_total:.3f} meters")
        if self.penetration_total >= self.armor_plate.total_thickness:
            print("Projectile fully penetrated all layers!")
        else:
            print("Projectile did not fully penetrate all layers.")
        print(f"Total fragments: {len(self.projectile.fragments)}")
        print(f"Block-by-block log saved to: {self.log_file}")

# -------------------------
# Example usage
# -------------------------
if __name__ == "__main__":
    proj = Projectile(name="APFSDS", material="tungsten", mass=10.0, length=1.2,
                      diameter=0.03, velocity=1500, tip_type="pointed")

    layers = [
        ArmorLayer([ArmorBlock("steel", 0.15, 0), ArmorBlock("steel", 0.05, 10)]),
        ArmorLayer([ArmorBlock("ceramic", 0.05, 0)]),
        ArmorLayer([ArmorBlock("steel", 0.1, 0)])
    ]

    plate = ArmorPlate(layers)

    sim = PenetrationSimulation(proj, plate, block_size=0.01)
    sim.run()