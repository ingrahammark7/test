# === Part 1: Imports and Utilities ===
import math
import random
import sys
import numpy as np

deadtargets = {}

def angle_diff(a, b):
    """Minimal difference between two angles in degrees."""
    diff = (a - b + 180) % 360 - 180
    return diff

maxtime = 30000

# --- Radar class ---
class Radar:
    def __init__(self, max_range_km=50, base_detection_prob=0.9):
        self.max_range_km = max_range_km
        self.base_detection_prob = base_detection_prob
        self.jamming_level = 0.0

    def set_jamming_level(self, level):
        self.jamming_level = max(0.0, min(1.0, level))

    def detect(self, own_position, target_position, target_rcs):
        dx = target_position[0] - own_position[0]
        dy = target_position[1] - own_position[1]
        distance = math.hypot(dx, dy)
        if distance > self.max_range_km:
            return False

        detection_chance = self.base_detection_prob * (1 - distance / self.max_range_km)
        rcs_factor = target_rcs / 5.0
        detection_chance *= min(2.0, rcs_factor)
        detection_chance *= (1 - self.jamming_level)
        detection_chance = max(0.0, min(1.0, detection_chance))
        return random.random() < detection_chance

class EnemyAircraft:
    def __init__(self, eid, aircraft_type, position, heading, speed, altitude, rcs):
        self.id = eid
        self.type = aircraft_type
        self.position = position
        self.heading = heading
        self.speed = speed
        self.altitude = altitude
        self.rcs = rcs
        self.alive = True

    def update_position(self, time_sec=1.0):
        if not self.alive:
            return
        dist_km = self.speed * (time_sec / 3600)
        rad = math.radians(self.heading)
        dx = dist_km * math.cos(rad)
        dy = dist_km * math.sin(rad)
        x, y = self.position
        self.position = (x + dx, y + dy)

    def status(self):
        x, y = self.position
        return f"{self.id} [{self.type}] Pos: ({x:.1f}, {y:.1f}) Alt: {self.altitude:.0f}m Speed: {self.speed:.0f}km/h"

def generate_random_enemies(n=5):
    enemies = []
    for i in range(n):
        is_bomber = random.random() < 0.4
        enemy = EnemyAircraft(
            eid=f"Enemy{i+1}",
            aircraft_type="bomber" if is_bomber else "fighter",
            position=(random.uniform(30, 100), random.uniform(-50, 50)),
            heading=random.uniform(180, 360),
            speed=random.uniform(700, 900) if is_bomber else random.uniform(1100, 1400),
            altitude=random.uniform(8000, 13000),
            rcs=random.uniform(8, 15) if is_bomber else random.uniform(1.5, 4.0)
        )
        enemies.append(enemy)
    return enemies
class Missile:
    def __init__(self, launcher, target):
        self.launcher = launcher
        self.target = target
        self.position = launcher.position
        self.speed = 3000  # km/h approx Mach 2.5
        self.alive = True
        self.max_turn_rate = 20  # degrees per second
        self.heading = launcher.heading

    def update(self, time_sec=1.0):
        if not self.alive or not self.target.alive:
            self.alive = False
            return

        # Guidance: turn heading towards target within max turn rate
        desired_heading = self._bearing_to_point(self.target.position)
        diff = angle_diff(desired_heading, self.heading)

        max_turn = self.max_turn_rate * time_sec
        if abs(diff) > max_turn:
            diff = max_turn if diff > 0 else -max_turn
        self.heading = (self.heading + diff) % 360

        # Move forward
        dist_km = self.speed * (time_sec / 3600)
        rad = math.radians(self.heading)
        dx = dist_km * math.cos(rad)
        dy = dist_km * math.sin(rad)
        x, y = self.position
        self.position = (x + dx, y + dy)

        # Check for hit (within 0.2 km)
        if self._distance_to_point(self.target.position) < 0.2:
            hit_chance = 0.8
            if random.random() < hit_chance:
                print(f"Missile from {self.launcher.name} hit {self.target.id}!")
                deadtargets.setdefault(self.target.id)
                self.target.alive = False
                return self.target.id
            else:
                print(f"Missile from {self.launcher.name} missed {self.target.id}.")
            self.alive = False

    def _distance_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.hypot(dx, dy)

    def _bearing_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.degrees(math.atan2(dy, dx)) % 360

class MiG25:
    def __init__(self, name):
        self.name = name
        self.heading = 0.0
        self.altitude = 12000.0
        self.speed = 1500.0
        self.position = (0.0, 0.0)
        self.weapons_fired = 0
        self.max_fire_range = 20.0
        self.rtb_mode = False
        self.fuel = 18000  # kg
        self.fuel_burn_rate = 0.5 # kg/sec
        self.command_failure_chance = 0.1
        self.current_missile = None
        self.evasive = False
        self.evasive_time = 0
        self.alive=1

        self.radar = Radar(max_range_km=60, base_detection_prob=0.95)

    def set_jamming(self, level):
        self.radar.set_jamming_level(level)

    def _distance_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.hypot(dx, dy)

    def _bearing_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.degrees(math.atan2(dy, dx)) % 360

    def detect_target(self, target):
        return self.radar.detect(self.position, target.position, target.rcs)

    def receive_gci_command(self, target):
        if random.random() < self.command_failure_chance:
            print(f"{self.name} GCI command disrupted by ECM!")
            return
        self.heading = self._bearing_to_point(target.position)

    def update_position(self, time_sec=1.0):
        if self.fuel <= 0:
            self.speed = 0
            self.rtb_mode = True
            print(f"{self.name} OUT OF FUEL - Forced RTB")
            return
        burn = self.fuel_burn_rate * time_sec * (2 if self.evasive else 1)
        self.fuel -= burn

        dist_km = self.speed * (time_sec / 3600)
        rad = math.radians(self.heading)
        dx = dist_km * math.cos(rad)
        dy = dist_km * math.sin(rad)
        x, y = self.position
        self.position = (x + dx, y + dy)

        if self.evasive:
            self.evasive_time -= time_sec
            if self.evasive_time <= 0:
                self.evasive = False

    def launch_missile(self, target):
        if self.current_missile and self.current_missile.alive:
            return False
        distance = self._distance_to_point(target.position)
        if distance > self.max_fire_range:
            return False
        self.weapons_fired += 1
        self.current_missile = Missile(self, target)
        print(f"{self.name} launched missile at {target.id}")
        self.evasive = True
        self.evasive_time = 10
        self.fuel -= 0
        return True

    def update_missile(self):
        if self.current_missile and self.current_missile.alive:
            return self.current_missile.update()

    def status(self):
        x, y = self.position
        mode = "RTB" if self.rtb_mode else ("EVASIVE" if self.evasive else "NORMAL")
        return (f"{self.name}: Pos=({x:.1f},{y:.1f}) Alt={self.altitude:.0f}m "
                f"Heading={self.heading:.1f} Speed={self.speed:.0f} "
                f"Weapons Fired={self.weapons_fired} Fuel={self.fuel:.0f}kg Mode={mode}")
class MiG23:
    def __init__(self, name):
        self.name = name
        self.heading = 0.0
        self.altitude = 9000.0
        self.speed = 1350.0
        self.position = (0.0, 0.0)
        self.weapons_fired = 0
        self.max_fire_range = 3.0  # guns only
        self.rtb_mode = False
        self.fuel = 15000  # kg
        self.fuel_burn_rate = 0.4# kg/sec
        self.command_failure_chance = 0.1
        self.dogfight_mode = False
        self.alive=1

        self.radar = Radar(max_range_km=30, base_detection_prob=0.8)

    def set_jamming(self, level):
        self.radar.set_jamming_level(level)

    def _distance_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.hypot(dx, dy)

    def _bearing_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.degrees(math.atan2(dy, dx)) % 360

    def detect_target(self, target):
        return self.radar.detect(self.position, target.position, target.rcs)

    def receive_gci_command(self, target):
        if random.random() < self.command_failure_chance:
            print(f"{self.name} GCI command disrupted by ECM!")
            return
        if not self.dogfight_mode:
            self.heading = self._bearing_to_point(target.position)

    def update_position(self, time_sec=1.0):
        if self.fuel <= 0:
            self.speed = 0
            self.rtb_mode = True
            print(f"{self.name} OUT OF FUEL - Forced RTB")
            return

        fuel_burn = self.fuel_burn_rate * time_sec
        if self.dogfight_mode:
            fuel_burn *= 1.5
            self.heading = (self.heading + random.uniform(-10, 10)) % 360
        self.fuel -= fuel_burn

        dist_km = self.speed * (time_sec / 3600)
        rad = math.radians(self.heading)
        dx = dist_km * math.cos(rad)
        dy = dist_km * math.sin(rad)
        x, y = self.position
        self.position = (x + dx, y + dy)

    def attempt_gun_fire(self, target):
        if not target.alive:
            return False
        distance = self._distance_to_point(target.position)
        if distance > self.max_fire_range:
            return False
        bearing = self._bearing_to_point(target.position)
        bearing_diff = abs(angle_diff(bearing, self.heading))
        if bearing_diff > 10:
            return False
        self.weapons_fired += 1
        hit = random.random() < 0.6
        if hit:
            print(f"{self.name} fired guns and hit {target.id} at {distance:.1f} km!")
            target.alive = False
        else:
            print(f"{self.name} fired guns and missed {target.id} at {distance:.1f} km.")
        return True

    def status(self):
        x, y = self.position
        mode = "DOGFIGHT" if self.dogfight_mode else "GCI"
        return (f"{self.name}: Pos=({x:.1f},{y:.1f}) Alt={self.altitude:.0f}m "
                f"Heading={self.heading:.1f} Speed={self.speed:.0f} "
                f"Weapons Fired={self.weapons_fired} Fuel={self.fuel:.0f}kg Mode={mode}")
class GroundTarget:
    def __init__(self, tid, position, health=100):
        self.id = tid
        self.position = position
        self.health = health
        self.alive = True

    def take_damage(self, dmg):
        self.health -= dmg
        if self.health <= 0:
            self.alive = False
            print(f"*** Ground target {self.id} destroyed! ***")

    def status(self):
        x, y = self.position
        return f"Ground Target {self.id}: Pos=({x:.1f},{y:.1f}) Health={self.health}"


class GlideBomb:
    def __init__(self, position, target):
        self.position = position
        self.target = target
        self.speed = 600  # km/h glide speed
        self.alive = True

    def update(self, time_sec=1):
        if not self.alive or not self.target.alive:
            self.alive = False
            return
        dx = self.target.position[0] - self.position[0]
        dy = self.target.position[1] - self.position[1]
        dist = math.hypot(dx, dy)
        if dist < 0.1:
            print(f"Glide bomb hit {self.target.id}!")
            self.target.take_damage(50)
            self.alive = False
            return
        move_dist = (self.speed * time_sec) / 3600
        self.position = (self.position[0] + dx / dist * move_dist,
                         self.position[1] + dy / dist * move_dist)


class MiG27:
    def __init__(self, name):
        self.name = name
        self.position = (0, 0)
        self.heading = 0
        self.speed = 1300
        self.fuel = 16000
        self.guns_fired = 0
        self.glide_bombs = []
        self.weapons_fired = 0
        self.rtb_mode = False
        self.target_ground = None
        self.alive=1

    def _distance_to_point(self, point):
        dx = point[0] - self.position[0]
        dy = point[1] - self.position[1]
        return math.hypot(dx, dy)

    def select_ground_target(self, targets):
        alive_targets = [t for t in targets if t.alive]
        if alive_targets:
            self.target_ground = random.choice(alive_targets)
            print(f"{self.name} selected ground target {self.target_ground.id}")
        else:
         	print("RTB ", self.name)
         	self.rtb_mode=1
    def attack_ground_target(self):
        if self.target_ground and self.fuel > 0:
            bomb = GlideBomb(position=self.position, target=self.target_ground)
            self.glide_bombs.append(bomb)
            print(f"{self.name} launched glide bomb at {self.target_ground.id}")
            self.fuel -= 0# bomb launch fuel cost
            self.weapons_fired += 1

    def update(self, time_sec=1):
        if self.fuel <= 0:
            self.speed = 0
            self.rtb_mode = True
            print(f"{self.name} out of fuel!")
            return
        if(self.rtb_mode):
        	return
        self.fuel -= 0.4* time_sec
        dx =  self.target_ground.position[0]-self.position[0]
        dy =  self.target_ground.position[1]-self.position[1]
        if(self.target_ground.alive==1):
        	
        	self.heading=math.degrees(math.atan2(dx,dy))
        	print(self.heading)
        
        if(abs(self.position[0])>100):
        	print(self.target_ground.position)
        	sys.exit()
        if(dy==-1):
        	dy=0
        print(dx)
        print(dy)
        sl=(dx/(dy+1))/(dx+dy)
        dist = self.speed * time_sec / 3600
        sl=sl*dist
        sx=sl*dx
        sy=(1-sl)*dy
        if(dx==0):
        	sx=0
        	sy=dist
        print(dist)
        self.position = (self.position[0] + sx,
        self.position[1] + sy)	
        # Update glide bombs
        for bomb in self.glide_bombs:
            if bomb.alive:
                bomb.update(time_sec)
        # Remove spent bombs
        self.glide_bombs = [b for b in self.glide_bombs if b.alive]

    def status(self):
        x, y = self.position
        return (f"{self.name}: Pos=({x:.1f},{y:.1f}) Speed={self.speed:.0f} "
                f"Fuel={self.fuel:.0f} GlideBombs={len(self.glide_bombs)} "
                f"Weapons Fired={self.weapons_fired} RTB={self.rtb_mode}")
def generate_debrief(migs, enemies, ground_targets, starten,sams):
    print("\n=== MISSION DEBRIEF ===\n")

    total_sorties = len(migs)
    total_weapons_fired = sum(m.weapons_fired for m in migs)
    total_rtb = sum(1 for m in migs if m.rtb_mode or m.fuel <= 0 or m.speed == 0)

    enemy_kills = sum(1 for e in enemies if not e.alive)
    ground_kills = sum(1 for g in ground_targets if not g.alive)

    print(f"Total Sorties: {total_sorties}")
    print(f"Enemy Aircraft Destroyed: {starten-len(enemies)} / {starten}")
    print(f"Ground Targets Destroyed: {ground_kills} / {len(ground_targets)}")
    print(f"Total Weapons Fired: {total_weapons_fired}")
    print(f"Sorties that Returned to Base or Landed: {total_rtb} / {total_sorties}")

    print("\n--- Pilot Status ---")
    for m in migs:
        status = "LANDED" if m.speed == 0 else "RTB" if m.rtb_mode else "IN AIR"
        print(f"{m.name}: Weapons Fired={m.weapons_fired}, Fuel Left={m.fuel:.0f}kg, Status={status}")

    print("\n--- Enemy Survivors ---")
    for e in enemies:
        if e.alive:
            print(f"{e.id} [{e.type}] Pos=({e.position[0]:.1f}, {e.position[1]:.1f}) Alt={e.altitude:.0f}m")

    print("\n--- Ground Targets Remaining ---")
    for g in ground_targets:
        if g.alive:
            print(f"{g.id} Pos=({g.position[0]:.1f}, {g.position[1]:.1f})")
    
    if sams:
        print("\n--- Ground Defense Summary ---")
        for sam in sams:
            print(f"{sam.name}: Cooldown Remaining={sam.cooldown:.1f}s")

    print("\n=== END OF DEBRIEF ===")

class GroundDefense:
    def __init__(self, name, position, detection_range_km, fire_range_km, cooldown_time, hit_chance=0.5):
        self.name = name
        self.position = position
        self.detection_range_km = detection_range_km
        self.fire_range_km = fire_range_km
        self.cooldown = 0
        self.cooldown_time = cooldown_time
        self.hit_chance = hit_chance

    def _distance_to(self, aircraft):
        dx = aircraft.position[0] - self.position[0]
        dy = aircraft.position[1] - self.position[1]
        return math.hypot(dx, dy)

    def engage(self, aircraft, time_step=1.0):
        if self.cooldown > 0:
            self.cooldown -= time_step
            return
        if not aircraft.alive:
            return
        dist = self._distance_to(aircraft)
        if dist < self.fire_range_km:
            self.cooldown = self.cooldown_time
            print(f"{self.name} fires at {aircraft.name}")
            evade_penalty = 0.5 if getattr(aircraft, "evasive", False) else 1.0
            if random.random() < self.hit_chance * evade_penalty:
                aircraft.alive = False
                print(f"{aircraft.name} was destroyed by {self.name}!")

def main():
    # Create aircraft
    mig25s = [MiG25(f"MiG25_{i+1}") for i in range(2)]
    mig23s = [MiG23(f"MiG23_{i+1}") for i in range(2)]
    mig27s = [MiG27(f"MiG27_{i+1}") for i in range(1)]

    enemies = generate_random_enemies(6)
    starten = len(enemies)
    ground_targets = [GroundTarget(f"GT{i+1}", (random.uniform(10, 40), random.uniform(-20, 20))) for i in range(3)]

    # Initialize SAM ground defenses
    sams = [
        GroundDefense("SAM1", (25, 5), detection_range_km=40, fire_range_km=10, cooldown_time=100, hit_chance=0),
        GroundDefense("SAM2", (35, -10), detection_range_km=35, fire_range_km=8, cooldown_time=80, hit_chance=0),
    ]

    max_time = maxtime  # seconds
    time_step = 1

    for t in range(0, max_time, time_step):
        print(f"\n=== Time {t}s ===")

        # Update enemy aircraft
        for enemy in enemies:
            enemy.update_position(time_step)
            if enemy.alive:
                print(enemy.status())

        # MiG-25 actions
        for mig in mig25s:
            if mig.rtb_mode or not mig.alive:
                continue
            live_targets = [e for e in enemies if e.alive]
            if not live_targets:
                mig.rtb_mode = True
                print(f"{mig.name} RTB: All targets destroyed")
                continue
            target = min(live_targets, key=lambda e: mig._distance_to_point(e.position))
            if target.id in deadtargets:
                target.alive = False
            if mig.detect_target(target):
                mig.receive_gci_command(target)
                if not mig.launch_missile(target):
                    pass
                else:
                    mig.launch_missile(target)
            else:
                print(f"{mig.name} lost target detection.")
            mig.update_position(time_step)
            missile_result = mig.update_missile()
            if missile_result is not None:
                for e in enemies:
                    if e.id == missile_result:
                        e.alive = False

            enemies = [e for e in enemies if e.alive]
            print(mig.status())

        # MiG-23 actions
        for mig in mig23s:
            if mig.rtb_mode or not mig.alive:
                continue
            live_targets = [e for e in enemies if e.alive]
            if not live_targets:
                mig.rtb_mode = True
                print(f"{mig.name} RTB: All targets destroyed")
                continue
            target = min(live_targets, key=lambda e: mig._distance_to_point(e.position))
            mig.receive_gci_command(target)
            if mig._distance_to_point(target.position) < 5:
                mig.dogfight_mode = True
                mig.attempt_gun_fire(target)
            else:
                mig.dogfight_mode = False
            mig.update_position(time_step)
            print(mig.status())

        # MiG-27 ground attack
        # Ground defense engagements
        for sam in sams:
            for mig in mig25s + mig23s + mig27s:
                if mig.alive:
                    sam.engage(mig, time_step)
        for mig in mig27s:
            if mig.fuel <= 0 or not mig.alive or mig.rtb_mode:
                continue
            if mig.target_ground is None or not mig.target_ground.alive:
                mig.select_ground_target(ground_targets)
            if mig.target_ground and mig._distance_to_point(mig.target_ground.position) < 25:
                mig.attack_ground_target()
            mig.update(time_step)
            print(mig.status())

        # Ground defense engagements (SAMs)
        for sam in sams:
            for mig in mig25s + mig23s + mig27s:
                if mig.alive:
                    sam.engage(mig, time_step)

        # Optional: Stop simulation early if no enemies or no MiGs alive
        if(t==max_time-1):
        	generate_debrief(mig25s + mig23s + mig27s, enemies, ground_targets, starten, sams=sams)
        if not any(e.alive for e in enemies) or not any(mig.alive for mig in mig25s + mig23s + mig27s):
            print("\nAll air combatants have been neutralized or MiGs out of fuel/life. Ending mission.")
            generate_debrief(mig25s + mig23s + mig27s, enemies, ground_targets, starten, sams=sams)
            break
  
            
            


if __name__ == "__main__":
    main()
                
               