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
    def __init__(self, name, hp, turrets, armor_zones, accuracy, max_range_km, speed_kts, fire_strategy="standard"):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.turrets = turrets
        self.armor_zones = armor_zones
        self.accuracy = accuracy
        self.max_range = max_range_km
        self.speed = speed_kts
        self.strategy = fire_strategy
        self.distance_km = max_range_km  # starting distance
        self.fires = 0
        self.disabled_turrets = 0
        self.log = []

    def move(self, target_distance, tactic="standard"):
        if tactic == "close":
            self.distance_km = max(0, self.distance_km - self.speed/60)
        elif tactic == "keep_distance":
            self.distance_km = min(self.max_range, self.distance_km + self.speed/60)
        # standard: adjust slightly
        elif tactic == "standard":
            delta = (target_distance - self.distance_km) * 0.5
            self.distance_km += delta
            self.distance_km = max(0, min(self.distance_km, self.max_range))

    def apply_fire_damage(self):
        fire_damage = self.fires * 0.02 * self.max_hp
        self.hp -= fire_damage
        if self.fires > 0:
            self.log.append(f"{self.name} suffers {fire_damage:.1f} fire damage!")

    def fire(self, target, weather_factor=1.0, sea_state_factor=1.0):
        hits = 0
        damage = 0
        if self.hp <= 0:
            return hits, damage  # cannot fire if destroyed
        for turret in self.turrets:
            if turret.ready_in <= 0 and self.disabled_turrets < len(self.turrets):
                for _ in range(turret.shells_per_min):
                    effective_accuracy = self.accuracy * max(0.05, 1 - self.distance_km / self.max_range)
                    effective_accuracy *= weather_factor * sea_state_factor
                    if random.random() < effective_accuracy:
                        zone = random.choice(target.armor_zones)
                        # Armor slope effect: reduce penetration by 20% chance
                        if random.random() < 0.2:
                            effective_caliber = turret.caliber * 0.8
                        else:
                            effective_caliber = turret.caliber
                        if effective_caliber > zone.thickness:
                            dmg = 50 * zone.hp_multiplier
                            target.hp -= dmg
                            hits += 1
                            damage += dmg
                            if random.random() < 0.03:
                                target.fires += 1
                                target.log.append(f"{target.name} caught fire!")
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
        if random.random() < 0.01:
            self.disabled_turrets += 1
            self.log.append(f"{self.name} has a turret disabled!")
        return hits, damage

# === Fleet Functions ===

def fleet_hp(fleet):
    return sum([ship.hp for ship in fleet])

def fleet_alive(fleet):
    return [ship for ship in fleet if ship.hp > 0]

def select_target(attacker, enemy_fleet):
    # AI targeting: prioritize strongest enemy or nearest
    alive = fleet_alive(enemy_fleet)
    if not alive:
        return None
    # Priority: largest gun (approx by turret caliber)
    alive.sort(key=lambda s: max([t.caliber for t in s.turrets]), reverse=True)
    return alive[0]

# === Ship Definitions ===

def create_uss_iowa():
    turrets = [Turret(f"Turret{i+1}", 3, 1, 406) for i in range(4)]
    armor = [ArmorZone("Belt", 310), ArmorZone("Deck", 150), ArmorZone("Turret", 406)]
    return Battleship("USS Iowa", 1000, turrets, armor, 0.25, 24, 33, "standard")

def create_yamato():
    turrets = [Turret(f"Turret{i+1}", 2, 1, 460) for i in range(3)]
    armor = [ArmorZone("Belt", 410), ArmorZone("Deck", 200), ArmorZone("Turret", 650)]
    return Battleship("Yamato", 1200, turrets, armor, 0.2, 27, 27, "close")

def create_bismarck():
    turrets = [Turret(f"Turret{i+1}", 2, 1, 380) for i in range(3)]
    armor = [ArmorZone("Belt", 320), ArmorZone("Deck", 150), ArmorZone("Turret", 360)]
    return Battleship("Bismarck", 1100, turrets, armor, 0.22, 23, 30, "standard")

# === Simulation ===

def simulate_fleet_battle(fleet1, fleet2, max_minutes=60, weather=1.0, sea_state=1.0, day_visibility=1.0):
    history1 = []
    history2 = []

    print(f"Fleet Battle Start: {[s.name for s in fleet1]} vs {[s.name for s in fleet2]}\n")

    for minute in range(1, max_minutes+1):
        # Movement AI
        for ship in fleet1:
            target = select_target(ship, fleet2)
            if target:
                ship.move(target.distance_km, tactic=ship.strategy)
        for ship in fleet2:
            target = select_target(ship, fleet1)
            if target:
                ship.move(target.distance_km, tactic=ship.strategy)

        # Apply fire damage (fires) first
        for ship in fleet1 + fleet2:
            ship.apply_fire_damage()

        # Fire phase
        for ship in fleet1:
            target = select_target(ship, fleet2)
            if target:
                ship.fire(target, weather*day_visibility, sea_state)
        for ship in fleet2:
            target = select_target(ship, fleet1)
            if target:
                ship.fire(target, weather*day_visibility, sea_state)

        # Track fleet HP
        history1.append(fleet_hp(fleet1))
        history2.append(fleet_hp(fleet2))

        # Print summary per minute
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
    plt.title("Fleet Battle Simulation")
    plt.legend()
    plt.show()

    # Print individual ship logs
    print("\nEvent Logs:")
    for ship in fleet1 + fleet2:
        for e in ship.log:
            print(f"{ship.name}: {e}")

# === Run Fleet Battle Example ===

fleet1 = [create_uss_iowa()]
fleet2 = [create_yamato(), create_bismarck()]

simulate_fleet_battle(fleet1, fleet2, max_minutes=60, weather=0.9, sea_state=0.95, day_visibility=0.8)