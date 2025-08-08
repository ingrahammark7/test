# nuct_restore.py
import sympy as sp
import math

# Attempt import from your pen.py
from pen import Material  # expects your pen.py to provide getsteel/getdu and Material
import pen

class NuclearPenetrationModel:
    def __init__(self, material):
        self.material = material
        
        # Symbolic variables (kept for compatibility with older code)
        self.E = sp.symbols('E')        # Particle energy in MeV
        self.n_e = sp.symbols('n_e')    # Electron density proxy
        
        self.phi = sp.GoldenRatio
        # Physical constants (kept your original expressions)
        self.alpha_fs = 1/((((4*sp.pi)-6)**self.phi)**self.phi)  # fine-structure-like proxy
        self.alpha = 1 / self.alpha_fs
        self.am = self.alpha ** self.phi
        self.osc = 6
        self.brem = self.am * (self.alpha ** (1 + ((1/((self.osc-1)*(self.osc-2))))))
        self.disc = self.brem * 16
        self.shellt = self.brem / 3
        self.compt = self.brem * 2
        self.evperj = pen.getsteel().ev_to_joule

        # Planck-ish proxy values (kept your formula)
        self.pm = self.alpha ** self.phi ** 4.55
        self.ac = self.pm       
        self.prma = 1 / (self.alpha ** self.phi ** 5)
        self.prma = self.prma / 1000
        self.pm = self.pm * self.prma
        self.ec = material.elementary_charge
        self.c=3e8

    def bremsstrahlung_loss(self, E_mev, n_e):
        # Keep your original numeric form (returns a float)
        Z = self.material.atomic_number
        E_mev = math.sqrt(E_mev)
        frac = E_mev / (self.compt)
        exponent = frac * self.osc
        
        # this is your original expression (numeric)
        loss = (Z ** exponent) * n_e * self.alpha_fs * math.log(E_mev + 1)
        return loss

    def emf(self, mass1, mass2, r):
        c1 = mass1 / self.prma * self.ec
        c2 = mass2 / self.prma * self.ec
        top = pen.getsteel().k * c1 * c2
        return top / r

    def velfromen(self, mass, en):
        # en assumed joules here
        return math.sqrt(2 * (en / mass))

    def emvf(self, mass1, mass2, r):
        emff = self.emf(mass1, mass2, r)
        v1 = self.velfromen(mass1, emff)
        v2 = self.velfromen(mass2, emff)
        return min(v1,v2)

    def mhd_bolus(self, E_mev, round_energy_mj, round_diameter_cm, round_mas, round_ld):
        # Keep your original structure; small safety for ch1
        numpm = round_mas / self.pm
        perpm = round_energy_mj / numpm if numpm != 0 else 0
        numpm = math.sqrt(numpm)
        peaken = numpm * perpm
        ch1 = getattr(pen.getsteel(), "ch1", None)
        if ch1 is None:
            # fallback constant if your pen.getsteel() doesn't define ch1
            ch1 = 1.0
        charger = (peaken / numpm) / ch1 if numpm != 0 else 0.0
        if charger > 1:
            print("ionization achieved")
        else:
            return 0
        length = round_ld * round_diameter_cm / 100.0
        length = length / 2.0
        en = round_energy_mj * 1_000_000.0
        roundspeed = self.velfromen(round_mas, en)
        print("speed ", roundspeed)
        em=self.emvf(round_mas,self.pm,length)
        print("flux flies at c% ",em/self.c)
        em1=em**(1/3)
        print("round speed % of flux",roundspeed/(em1))
        # placeholder return (preserve your placeholder behavior)
        return 1

    def honeycomb_dissipation_factor(self, layers):
        return (1 + layers) ** 3

    def mjtomev(self, num):
        return num * 6.242e12

    def roundld(self, round_diameter_cm, round_mas):
        # Keep your older (square area) method as you originally had it
        round_front_vol = round_diameter_cm * round_diameter_cm / 1000000.0
        round_front_mass = round_front_vol * self.material.density
        # avoid division by zero
        if round_front_mass == 0:
            return 1
        return round_mas / round_front_mass

    def penetration(self, round_energy_mj, round_diameter_cm, honeycomb_layers, round_mas):
        round_ld = self.roundld(round_diameter_cm, round_mas)
        print("round ld ", round_ld)
        E_mev_val = self.mjtomev(round_energy_mj)

        # electron density proxy proportional to material density (keep your original scaling)
        n_e_val = self.material.density * (1 / self.am)

        # use numeric bremsstrahlung (no sympy subs/eval)
        brems_loss_val = self.bremsstrahlung_loss(E_mev_val, n_e_val)

        base_penetration = (round_energy_mj / self.material.material_energy_density_mj_per_hvl) * self.material.base_hvl_cm

        dissipation = self.honeycomb_dissipation_factor(honeycomb_layers)

        # your original cap behaviour (keeps your logic)
        if brems_loss_val > E_mev_val:
            brems_loss_val = 0  # entire energy dissipated (your rule)

        mhd_var = self.mhd_bolus(E_mev_val, round_energy_mj, round_diameter_cm, round_mas, round_ld)

        # original precedence from your version: mhd_var + base / (1 + brems * dissipation)
        adjusted_penetration = mhd_var + base_penetration / (1 + brems_loss_val * dissipation)

        # Ensure penetration not below 1 HVL physically
        if adjusted_penetration < self.material.base_hvl_cm:
            adjusted_penetration = 0

        return float(adjusted_penetration)


def nuclear_penetration(round_energy_mj, round_diameter_cm, honeycomb_layers, round_mas, material_name="steel"):
    """
    Compute nuclear-effect-adjusted penetration depth (cm) for given round and armor.
    """
    if isinstance(material_name, Material):
        material = material_name
    else:
        mat_name = material_name.lower()
        if mat_name == "steel":
            material = pen.getsteel()
        elif mat_name == "du":
            material = pen.getdu()
        else:
            material = pen.getsteel()

    model = NuclearPenetrationModel(material)
    return model.penetration(round_energy_mj, round_diameter_cm, honeycomb_layers, round_mas)


if __name__ == "__main__":
    # Test/demo with your original numbers
    print("Testing nuclear penetration model...")

    round_energy = 10  # MJ
    round_diameter = 2.2  # cm
    round_mass = 2
    honeycomb = 0

    pen_steel = nuclear_penetration(round_energy, round_diameter, honeycomb, round_mass, "steel")
    pen_du = nuclear_penetration(round_energy, round_diameter, honeycomb, round_mass, "du")

    print(f"Estimated penetration in Steel: {pen_steel:.3f} cm")
    print(f"Estimated penetration in Depleted Uranium: {pen_du:.3f} cm")