import random
import matplotlib.pyplot as plt

# ===============================
# Classes
# ===============================

class ArmorZone:
    def __init__(self, name, thickness, hp):
        self.name = name
        self.thickness = thickness
        self.hp = hp

class Turret:
    def __init__(self, name, shells_per_min, reload_time, caliber, ammo_stock=100):
        self.name = name
        self.shells_per_min = shells_per_min
        self.reload_time = reload_time
        self.caliber = caliber
        self.ready_in = 0
        self.disabled = False
        self.ammo_stock = ammo_stock

class Battleship:
    def __init__(self, name, armor_zones, turrets, max_hp, accuracy, max_range, speed_kts,
                 strategy="standard", fuel=1000):
        self.name = name
        self.armor_zones = armor_zones
        self.turrets = turrets
        self.max_hp = max_hp
        self.hp = max_hp
        self.accuracy = accuracy
        self.max_range = max_range
        self.speed = speed_kts
        self.strategy = strategy
        self.distance_km = max_range
        self.fires = 0
        self.flooding = 0
        self.log = []
        self.retreat_threshold = 0.3
        self.ammo_type = "AP"
        self.engine_damage = 0
        self.fuel = fuel  # reduces speed if low
        self.pending_shells = []  # shells in flight

    # ===========================
    # Movement
    # ===========================
    def move(self, target_distance):
        if self.hp/self.max_hp < self.retreat_threshold or self.fuel < 0.2*self.max_hp:
            self.distance_km = min(self.max_range, self.distance_km + self.speed/60)
            self.log.append(f"{self.name} is retreating!")
        elif self.strategy == "close":
            self.distance_km = max(0, self.distance_km - (self.speed*(1-self.engine_damage)/60))
        elif self.strategy == "keep_distance":
            self.distance_km = min(self.max_range, self.distance_km + (self.speed*(1-self.engine_damage)/60))
        else:
            delta = (target_distance - self.distance_km) * 0.5
            self.distance_km = max(0, min(self.distance_km + delta, self.max_range))

    # ===========================
    # Fire / Ammo / Damage
    # ===========================
    def apply_fire_flooding(self):
        # damage over time
        fire_damage = self.fires * 0.02 * self.max_hp
        flood_damage = self.flooding * 0.015 * self.max_hp
        self.hp -= fire_damage + flood_damage
        if fire_damage > 0:
            self.log.append(f"{self.name} suffers {fire_damage:.1f} fire damage")
        if flood_damage > 0:
            self.log.append(f"{self.name} suffers {flood_damage:.1f} flooding damage")

    def repair(self):
        # Damage control reduces fires/flooding
        if self.fires > 0 and random.random() < 0.5:
            self.fires -= 1
            self.log.append(f"{self.name} extinguished a fire!")
        if self.flooding > 0 and random.random() < 0.3:
            self.flooding -= 1
            self.log.append(f"{self.name} reduced flooding!")

    def choose_ammo(self, zone):
        if zone.thickness > 400:
            self.ammo_type = "AP"
        else:
            self.ammo_type = "HE"

    def fire(self, target, weather=1.0, sea=1.0, visibility=1.0):
        if self.hp <= 0:
            return 0,0
        hits=0; damage=0
        for turret in self.turrets:
            if turret.disabled or turret.ready_in>0 or turret.ammo_stock<=0:
                turret.ready_in=max(0, turret.ready_in-1)
                continue
            for _ in range(min(turret.shells_per_min, turret.ammo_stock)):
                effective_acc=self.accuracy*max(0.05,1-self.distance_km/self.max_range)
                effective_acc*=weather*sea*visibility
                if random.random() < effective_acc:
                    zone=max(target.armor_zones,key=lambda z:z.thickness)
                    self.choose_ammo(zone)
                    effective_caliber = turret.caliber * (0.8 if self.ammo_type=="HE" else 1.0)
                    if random.random()<0.2: effective_caliber*=0.8
                    time_of_flight = self.distance_km/0.5 # simplified: 0.5 km/sec
                    self.pending_shells.append({'target':target,'zone':zone,'damage':50,'time':time_of_flight,'caliber':effective_caliber})
                    turret.ammo_stock-=1
            turret.ready_in=turret.reload_time
            if random.random()<0.01:
                turret.disabled=True
                self.log.append(f"{self.name} turret {turret.name} disabled!")
        return hits,damage

    def resolve_pending_shells(self):
        for shell in self.pending_shells[:]:
            shell['time']-=1
            if shell['time']<=0:
                target = shell['target']
                zone = shell['zone']
                dmg = shell['damage']
                target.hp-=dmg
                if random.random()<0.03:
                    target.fires+=1
                    target.log.append(f"{target.name} caught fire from delayed shell!")
                if random.random()<0.02:
                    target.flooding+=1
                    target.log.append(f"{target.name} flooding increased from delayed shell!")
                self.pending_shells.remove(shell)

# ===============================
# Fleet helpers
# ===============================

def fleet_alive(fleet):
    return [s for s in fleet if s.hp>0]

def fleet_hp(fleet):
    return sum(s.hp for s in fleet_alive(fleet))

def select_target(attacker,enemy_fleet):
    alive = fleet_alive(enemy_fleet)
    if not alive: return None
    alive.sort(key=lambda s: sum([t.caliber for t in s.turrets]), reverse=True)
    return alive[0]

# ===============================
# Ships
# ===============================

def create_uss_iowa():
    turrets=[Turret(f"T{i+1}",3,1,406) for i in range(4)]
    armor=[ArmorZone("Belt",310,310),ArmorZone("Deck",150,150),ArmorZone("Turret",406,406)]
    return Battleship("USS Iowa",armor,turrets,1000,0.25,24,33,"standard")

def create_yamato():
    turrets=[Turret(f"T{i+1}",2,1,460) for i in range(3)]
    armor=[ArmorZone("Belt",410,410),ArmorZone("Deck",200,200),ArmorZone("Turret",650,650)]
    return Battleship("Yamato",armor,turrets,1200,0.2,27,27,"close")

def create_bismarck():
    turrets=[Turret(f"T{i+1}",2,1,380) for i in range(3)]
    armor=[ArmorZone("Belt",320,320),ArmorZone("Deck",150,150),ArmorZone("Turret",360,360)]
    return Battleship("Bismarck",armor,turrets,1100,0.22,23,30,"standard")

# ===============================
# Ultimate Battle
# ===============================

def simulate_full_physics(fleet1,fleet2,max_minutes=60,weather=1.0,sea=1.0,visibility=1.0,seed=None):
    if seed: random.seed(seed)
    h1,h2=[],[]
    print(f"Ultimate Physics Fleet Battle Start: {[s.name for s in fleet1]} vs {[s.name for s in fleet2]}")
    for minute in range(1,max_minutes+1):
        for ship in fleet1+fleet2:
            ship.resolve_pending_shells()
        for ship in fleet1:
            t=select_target(ship,fleet2)
            if t: ship.move(t.distance_km)
        for ship in fleet2:
            t=select_target(ship,fleet1)
            if t: ship.move(t.distance_km)
        for ship in fleet1+fleet2:
            ship.apply_fire_flooding()
            ship.repair()
        for ship in fleet1:
            t=select_target(ship,fleet2)
            if t: ship.fire(t,weather,sea,visibility)
        for ship in fleet2:
            t=select_target(ship,fleet1)
            if t: ship.fire(t,weather,sea,visibility)
        h1.append(fleet_hp(fleet1))
        h2.append(fleet_hp(fleet2))
        print(f"Minute {minute}: Fleet1 HP={h1[-1]:.1f} Fleet2 HP={h2[-1]:.1f}")
        if h1[-1]<=0 and h2[-1]<=0: print("Draw!"); break
        elif h1[-1]<=0: print("Fleet 2 Wins!"); break
        elif h2[-1]<=0: print("Fleet 1 Wins!"); break
    plt.plot(h1,label="Fleet1");plt.plot(h2,label="Fleet2")
    plt.xlabel("Minutes");plt.ylabel("Fleet HP");plt.title("Ultimate Physics Fleet Battle");plt.legend();plt.show()
    print("\nEvent Logs:")
    for ship in fleet1+fleet2:
        for e in ship.log: print(f"{ship.name}: {e}")

# ===============================
# Example Run
# ===============================

fleet1=[create_uss_iowa()]
fleet2=[create_yamato(),create_bismarck()]

simulate_full_physics(fleet1,fleet2,max_minutes=60,weather=0.9,sea=0.95,visibility=0.8,seed=999)