import random
import matplotlib.pyplot as plt

# === Classes ===

class ArmorZone:
    def __init__(self, name, thickness, hp_multiplier=1.0):
        self.name = name
        self.thickness = thickness
        self.hp_multiplier = hp_multiplier

class Turret:
    def __init__(self, name, shells_per_min, reload_time, caliber):
        self.name = name
        self.shells_per_min = shells_per_min
        self.reload_time = reload_time
        self.caliber = caliber
        self.ready_in = 0

class Battleship:
    def __init__(self, name, hp, turrets, armor_zones, accuracy, max_range_km, speed_kts,
                 fire_strategy="standard"):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.turrets = turrets
        self.armor_zones = armor_zones
        self.accuracy = accuracy
        self.max_range = max_range_km
        self.speed = speed_kts
        self.strategy = fire_strategy
        self.distance_km = max_range_km
        self.fires = 0
        self.disabled_turrets = 0
        self.log = []
        self.flooding = 0
        self.retreat_threshold = 0.3  # retreat at 30% HP
        self.ammo_type = "AP"  # default ammo type

    def move(self, target_distance):
        """Move based on strategy and target distance"""
        if self.hp / self.max_hp < self.retreat_threshold:
            self.distance_km = min(self.max_range, self.distance_km + self.speed / 60)
            self.log.append(f"{self.name} is retreating!")
        elif self.strategy == "close":
            self.distance_km = max(0, self.distance_km - self.speed / 60)
        elif self.strategy == "keep_distance":
            self.distance_km = min(self.max_range, self.distance_km + self.speed / 60)
        else:
            delta = (target_distance - self.distance_km) * 0.5
            self.distance_km = max(0, min(self.distance_km + delta, self.max_range))

    def apply_fire_flooding_damage(self):
        """Damage from ongoing fires and flooding"""
        fire_damage = self.fires * 0.02 * self.max_hp
        flood_damage = self.flooding * 0.015 * self.max_hp
        total_damage = fire_damage + flood_damage
        self.hp -= total_damage
        if fire_damage > 0:
            self.log.append(f"{self.name} suffers {fire_damage:.1f} fire damage!")
        if flood_damage > 0:
            self.log.append(f"{self.name} suffers {flood_damage:.1f} flooding damage!")

    def choose_ammo(self, target_zone):
        """Select ammo based on target armor thickness"""
        if target_zone.thickness > 400:
            self.ammo_type = "AP"
        else:
            self.ammo_type = "HE"

    def fire(self, target, weather_factor=1.0, sea_state_factor=1.0):
        if self.hp <= 0:
            return 0, 0
        hits = 0
        damage = 0
        for turret in self.turrets:
            if turret.ready_in <= 0 and self.disabled_turrets < len(self.turrets):
                for _ in range(turret.shells_per_min):
                    effective_accuracy = self.accuracy * max(0.05, 1 - self.distance_km / self.max_range)
                    effective_accuracy *= weather_factor * sea_state_factor
                    if random.random() < effective_accuracy:
                        # Choose target armor zone intelligently
                        zone = max(target.armor_zones, key=lambda z: z.thickness)
                        self.choose_ammo(zone)
                        effective_caliber = turret.caliber
                        if self.ammo_type == "HE":
                            effective_caliber *= 0.8  # HE less effective at penetration
                        # Armor slope 20% chance to reduce penetration
                        if random.random() < 0.2:
                            effective_caliber *= 0.8
                        if effective_caliber > zone.thickness:
                            dmg = 50 * zone.hp_multiplier
                            target.hp -= dmg
                            hits += 1
                            damage += dmg
                            # Fire chance
                            if random.random() < 0.03:
                                target.fires += 1
                                target.log.append(f"{target.name} caught fire!")
                            # Flooding chance
                            if random.random() < 0.02:
                                target.flooding += 1
                                target.log.append(f"{target.name} flooding increased!")
                            # Critical hit
                            if random.random() < 0.05:
                                crit = dmg * 2
                                target.hp -= crit
                                damage += crit
                                self.log.append(f"Critical hit on {target.name}!")
                        else:
                            self.log.append(f"{self.name}'s shell failed to penetrate {zone.name} of {target.name}")
                turret.ready_in = turret.reload_time
            else:
                turret.ready_in -= 1
        # Turret malfunction
        if random.random() < 0.01:
            self.disabled_turrets += 1
            self.log.append(f"{self.name} has a turret disabled!")
        return hits, damage

# === Fleet Helper Functions ===

def fleet_alive(fleet):
    return [ship for ship in fleet if ship.hp > 0]

def fleet_hp(fleet):
    return sum(ship.hp for ship in fleet if ship.hp > 0)

def select_target(attacker, enemy_fleet):
    alive = fleet_alive(enemy_fleet)
    if not alive:
        return None
    # AI target selection: strongest remaining ship
    alive.sort(key=lambda s: max([t.caliber for t in s.turrets]), reverse=True)
    return alive[0]

# === Ship Definitions ===

def create_uss_iowa():  # Fleet 1 example
    turrets = [Turret(f"Turret{i+1}", 3, 1, 406) for i in range(4)]
    armor = [ArmorZone("Belt", 310), ArmorZone("Deck", 150), ArmorZone("Turret", 406)]
    return Battleship("USS Iowa", 1000, turrets, armor, 0.25, 24, 33, "standard")

def create_yamato():  # Fleet 2 example
    turrets = [Turret(f"Turret{i+1}", 2, 1, 460) for i in range(3)]
    armor = [ArmorZone("Belt", 410), ArmorZone("Deck", 200), ArmorZone("Turret", 650)]
    return Battleship("Yamato", 1200, turrets, armor, 0.2, 27, 27, "close")

def create_bismarck():  # Fleet 2 example
    turrets = [Turret(f"Turret{i+1}", 2, 1, 380) for i in range(3)]
    armor = [ArmorZone("Belt", 320), ArmorZone("Deck", 150), ArmorZone("Turret", 360)]
    return Battleship("Bismarck", 1100, turrets, armor, 0.22, 23, 30, "standard")

# === Fleet Battle Simulation ===

def simulate_fleet_battle(fleet1, fleet2, max_minutes=60, weather=1.0, sea_state=1.0, day_visibility=1.0, seed=None):
    if seed is not None:
        random.seed(seed)
    history1 = []
    history2 = []

    print(f"Fleet Battle Start: {[s.name for s in fleet1]} vs {[s.name for s in fleet2]}\n")

    for minute in range(1, max_minutes+1):
        # Movement
        for ship in fleet1:
            target = select_target(ship, fleet2)
            if target:
                ship.move(target.distance_km)
        for ship in fleet2:
            target = select_target(ship, fleet1)
            if target:
                ship.move(target.distance_km)

        # Apply fire/flooding damage
        for ship in fleet1 + fleet2:
            ship.apply_fire_flooding_damage()

        # Firing
        for ship in fleet1:
            target = select_target(ship, fleet2)
            if target:
                ship.fire(target, weather*day_visibility, sea_state)
        for ship in fleet2:
            target = select_target(ship, fleet1)
            if target:
                ship.fire(target, weather*day_visibility, sea_state)

        # Fleet HP tracking
        history1.append(fleet_hp(fleet1))
        history2.append(fleet_hp(fleet2))

        print(f"Minute {minute}: Fleet1 HP={history1[-1]:.1f}, Fleet2 HP={history2[-1]:.1f}")

        # Check for victory
        if history1[-1] <= 0 and history2[-1] <= 0:
            print("Both fleets destroyed! Draw.")
            break
        elif history1[-1] <= 0:
            print("Fleet 2 wins!")
            break
        elif history2[-1] <= 0:
            print("Fleet 1 wins!")
            break

    # Plot fleet HP over time
    plt.plot(history1, label="Fleet 1")
    plt.plot(history2, label="Fleet 2")
    plt.xlabel("Minutes")
    plt.ylabel("Fleet HP")
    plt.title("Ultimate Fleet Battle Simulation")
    plt.legend()
    plt.show()

    # Print detailed event logs
    print("\nEvent Logs:")
    for ship in fleet1 + fleet2:
        for event in ship.log:
            print(f"{ship.name}: {event}")

# === Example Usage ===

fleet1 = [create_uss_iowa()]
fleet2 = [create_yamato(), create_bismarck()]

simulate_fleet_battle(fleet1, fleet2, max_minutes=60, weather=0.9, sea_state=0.95, day_visibility=0.8, seed=42)