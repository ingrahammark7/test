import numpy as np
from scipy.integrate import quad

mu_0 = 4 * np.pi * 1e-7  # Vacuum permeability (T·m/A)

class MagnetSystemWithLosses:
    def __init__(self, m1, m2, r_start, r_snap, coil_resistance, hysteresis_loss, eddy_loss, mech_friction):
        self.m1 = m1
        self.m2 = m2
        self.r = r_start
        self.r_snap = r_snap
        self.is_on = False
        self.polarity = 1
        # Loss parameters (in Joules per cycle or per event)
        self.coil_resistance = coil_resistance  # energy lost turning on/off magnets
        self.hysteresis_loss = hysteresis_loss  # per magnetization cycle
        self.eddy_loss = eddy_loss  # per magnetization cycle
        self.mech_friction = mech_friction  # mechanical loss per movement

    def magnetic_energy(self, r):
        if not self.is_on or r == 0:
            return 0
        U = - (mu_0 / (4 * np.pi)) * (self.m1 * self.m2) / (r**3) * self.polarity
        return U

    def magnetic_force(self, r):
        if not self.is_on or r == 0:
            return 0
        F = 3 * (mu_0 / (4 * np.pi)) * (self.m1 * self.m2) / (r**4) * self.polarity
        return F

    def work_to_move(self, r1, r2):
        if not self.is_on:
            # Only mechanical friction losses apply
            distance = abs(r2 - r1)
            return self.mech_friction * distance
        integrand = lambda r: self.magnetic_force(r)
        ideal_work, _ = quad(integrand, r1, r2)
        # Add mechanical friction losses proportional to distance
        distance = abs(r2 - r1)
        total_work = ideal_work + self.mech_friction * distance
        return total_work

    def energy_to_turn_on(self, r):
        magnetic_energy = abs(self.magnetic_energy(r))
        # Add coil resistance, hysteresis, and eddy current losses
        total_loss = self.coil_resistance + self.hysteresis_loss + self.eddy_loss
        return magnetic_energy + total_loss

    def energy_released_turn_off(self, r):
        # Assume all stored magnetic energy released, but losses occur
        magnetic_energy = -self.magnetic_energy(r)
        total_loss = self.coil_resistance + self.hysteresis_loss + self.eddy_loss
        return magnetic_energy - total_loss  # losses reduce recovered energy

    def flip_polarity(self):
        # Flipping polarity costs energy equal to losses (simplified)
        self.polarity *= -1
        return self.coil_resistance + self.hysteresis_loss + self.eddy_loss

    def simulate_full_cycle(self):
        r_start = self.r
        r_snap = self.r_snap

        self.is_on = False
        work_off_move = self.work_to_move(r_start, r_snap)

        self.is_on = True
        energy_on = self.energy_to_turn_on(r_snap)

        r_contact = 0.001
        work_on_attract = self.work_to_move(r_snap, r_contact)
        kinetic_energy_snap = -work_on_attract

        energy_off = self.energy_released_turn_off(r_contact)
        self.is_on = False

        work_off_apart = self.work_to_move(r_contact, r_start)

        self.is_on = True
        energy_on_2 = self.energy_to_turn_on(r_start)

        flip_loss1 = self.flip_polarity()

        work_on_repel = self.work_to_move(r_start, r_snap)
        kinetic_energy_repel = -work_on_repel

        flip_loss2 = self.flip_polarity()

        energy_off_2 = self.energy_released_turn_off(r_snap)
        self.is_on = False

        total_energy_in = energy_on + energy_on_2 + work_off_move + work_off_apart + flip_loss1 + flip_loss2
        total_energy_out = kinetic_energy_snap + kinetic_energy_repel + energy_off + energy_off_2

        net_energy = total_energy_out - total_energy_in

        print(f"Energy to turn magnets ON at r_snap: {energy_on:.6e} J")
        print(f"Work moving magnets OFF (r_start to r_snap): {work_off_move:.6e} J")
        print(f"Work moving magnets ON attract (r_snap to contact): {work_on_attract:.6e} J")
        print(f"Kinetic energy from snap: {kinetic_energy_snap:.6e} J")
        print(f"Energy released turning magnets OFF at contact: {energy_off:.6e} J")
        print(f"Work moving magnets OFF apart (contact to r_start): {work_off_apart:.6e} J")
        print(f"Energy to turn magnets ON at r_start: {energy_on_2:.6e} J")
        print(f"Work moving magnets ON repel (r_start to r_snap): {work_on_repel:.6e} J")
        print(f"Kinetic energy from repel: {kinetic_energy_repel:.6e} J")
        print(f"Energy released turning magnets OFF at r_snap: {energy_off_2:.6e} J")
        print(f"Energy lost flipping polarity (2 flips): {flip_loss1 + flip_loss2:.6e} J")
        print(f"Net energy over full cycle with losses: {net_energy:.6e} J")


# Example realistic losses (Joules per cycle or event)
coil_resistance_loss = 1e-3    # 1 millijoule
hysteresis_loss = 1e-4         # 0.1 millijoule
eddy_current_loss = 5e-4        # 0.5 millijoule
mechanical_friction_per_meter = 1e-3  # 1 millijoule per meter moved

# System parameters
m1 = 0.1
m2 = 0.1
r_start = 0.1
r_snap = 0.01

system_with_losses = MagnetSystemWithLosses(
    m1, m2, r_start, r_snap,
    coil_resistance_loss,
    hysteresis_loss,
    eddy_current_loss,
    mechanical_friction_per_meter
)

system_with_losses.simulate_full_cycle()