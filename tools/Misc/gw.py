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
        self.fuel = fuel
        self.pending_shells = []

    # Movement
    def move(self, target_distance):
        effective_speed = self.speed * (1 - self.engine_damage) * (self.fuel / 1000)
        if self.hp/self.max_hp < self.retreat_threshold or self.fuel < 0.2*self.max_hp:
            self.distance_km = min(self.max_range, self.distance_km + effective_speed/60)
            self.log.append(f"{self.name} is retreating!")
        elif self.strategy == "close":
            self.distance_km = max(0, self.distance_km - effective_speed/60)
        elif self.strategy == "keep_distance":
            self.distance_km = min(self.max_range, self.distance_km + effective_speed/60)
        else:
            delta = (target_distance - self.distance_km) * 0.5
            self.distance_km = max(0, min(self.distance_km + delta, self.max_range))

    # Fires/Flooding damage over time
    def apply_fire_flooding(self):
        fire_damage = self.fires * 0.02 * self.max_hp
        flood_damage = self.flooding * 0.015 * self.max_hp
        self.hp -= fire_damage + flood_damage
        if fire_damage>0: self.log.append(f"{self.name} suffers {fire_damage:.1f} fire damage")
        if flood_damage>0: self.log.append(f"{self.name} suffers {flood_damage:.1f} flooding damage")

    # Repair/damage control
    def repair(self):
        if self.fires>0 and random.random()<0.5:
            self.fires-=1
            self.log.append(f"{self.name} extinguished a fire")
        if self.flooding>0 and random.random()<0.3:
            self.flooding-=1
            self.log.append(f"{self.name} reduced flooding")

    # Ammo selection
    def choose_ammo(self, zone):
        self.ammo_type="AP" if zone.thickness>400 else "HE"

    # Firing
    def fire(self, target, weather=1.0, sea=1.0, visibility=1.0):
        if self.hp<=0: return
        for turret in self.turrets:
            if turret.disabled or turret.ready_in>0 or turret.ammo_stock<=0:
                turret.ready_in=max(0, turret.ready_in-1)
                continue
            for _ in range(min(turret.shells_per_min,turret.ammo_stock)):
                eff_acc = self.accuracy*max(0.05,1-self.distance_km/self.max_range)
                eff_acc *= weather*sea*visibility
                if random.random()<eff_acc:
                    zone = max(target.armor_zones,key=lambda z:z.thickness)
                    self.choose_ammo(zone)
                    caliber = turret.caliber*(0.8 if self.ammo_type=="HE" else 1.0)
                    if random.random()<0.2: caliber*=0.8
                    tof = self.distance_km/0.5
                    self.pending_shells.append({'target':target,'zone':zone,'damage':50,'time':tof,'caliber':caliber})
                    turret.ammo_stock-=1
            turret.ready_in=turret.reload_time
            if random.random()<0.01:
                turret.disabled=True
                self.log.append(f"{self.name} turret {turret.name} disabled")

    # Resolve delayed shells
    def resolve_pending_shells(self):
        for shell in self.pending_shells[:]:
            shell['time']-=1
            if shell['time']<=0:
                target=shell['target']
                target.hp-=shell['damage']
                if random.random()<0.03:
                    target.fires+=1
                    target.log.append(f"{target.name} caught fire from delayed shell")
                if random.random()<0.02:
                    target.flooding+=1
                    target.log.append(f"{target.name} flooding increased from delayed shell")
                self.pending_shells.remove(shell)

# ===============================
# Fleet helpers
# ===============================
def fleet_alive(fleet): return [s for s in fleet if s.hp>0]
def fleet_hp(fleet): return sum(s.hp for s in fleet_alive(fleet))
def select_target(attacker,enemy_fleet):
    alive=fleet_alive(enemy_fleet)
    if not alive: return None
    alive.sort(key=lambda s: sum([t.caliber for t in s.turrets]), reverse=True)
    return alive[0]

# ===============================
# Ship constructors
# ===============================
def create_uss_iowa(): return Battleship("USS Iowa",[ArmorZone("Belt",310,310),ArmorZone("Deck",150,150),ArmorZone("Turret",406,406)],[Turret(f"T{i+1}",3,1,406) for i in range(4)],1000,0.25,24,33,"standard")
def create_missouri(): return Battleship("USS Missouri",[ArmorZone("Belt",305,305),ArmorZone("Deck",150,150),ArmorZone("Turret",406,406)],[Turret(f"T{i+1}",3,1,406) for i in range(3)],950,0.23,24,32,"standard")
def create_yamato(): return Battleship("Yamato",[ArmorZone("Belt",410,1100),ArmorZone("Deck",200,200),ArmorZone("Turret",650,650)],[Turret(f"T{i+1}",2,1,460) for i in range(3)],1100,0.2,27,27,"close")
def create_bismarck(): return Battleship("Bismarck",[ArmorZone("Belt",320,320),ArmorZone("Deck",150,150),ArmorZone("Turret",360,360)],[Turret(f"T{i+1}",2,1,380) for i in range(3)],900,0.22,23,30,"standard")

# ===============================
# Full Simulation
# ===============================
def simulate_full_physics(fleet1,fleet2,max_minutes=60,weather=1.0,sea=1.0,visibility=1.0,seed=None):
    if seed: random.seed(seed)
    h1,h2=[],[]
    print(f"Ultimate Balanced Fleet Battle: {[s.name for s in fleet1]} vs {[s.name for s in fleet2]}")
    for minute in range(1,max_minutes+1):
        for ship in fleet1+fleet2: ship.resolve_pending_shells()
        for ship in fleet1: t=select_target(ship,fleet2); 
        if t: ship.move(t.distance_km)
        for ship in fleet2: t=select_target(ship,fleet1)
        if t: ship.move(t.distance_km)
        for ship in fleet1+fleet2:
            ship.apply_fire_flooding()
            ship.repair()
        for ship in fleet1: t=select_target(ship,fleet2); 
        if t: ship.fire(t,weather,sea,visibility)
        for ship in fleet2: t=select_target(ship,fleet1)
        if t: ship.fire(t,weather,sea,visibility)
        h1.append(fleet_hp(fleet1)); h2.append(fleet_hp(fleet2))
        print(f"Minute {minute}: Fleet1 HP={h1[-1]:.1f} Fleet2 HP={h2[-1]:.1f}")
        if h1[-1]<=0 and h2[-1]<=0: print("Draw!"); break
        elif h1[-1]<=0: print("Fleet 2 Wins!"); break
        elif h2[-1]<=0: print("Fleet 1 Wins!"); break
    plt.plot(h1,label="Fleet1");plt.plot(h2,label="Fleet2")
    plt.xlabel("Minutes");plt.ylabel("Fleet HP");plt.title("Ultimate Balanced Physics Fleet Battle");plt.legend();plt.show()
    print("\nEvent Logs:")
    for ship in fleet1+fleet2:
        for e in ship.log: print(f"{ship.name}: {e}")

# ===============================
# Run Rebalanced Battle
# ===============================
fleet1=[create_uss_iowa(),create_missouri()]
fleet2=[create_yamato(),create_bismarck()]

simulate_full_physics(fleet1,fleet2,max_minutes=60,weather=0.9,sea=0.95,visibility=0.8,seed=999)