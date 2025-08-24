import math

droneheifh=10
dronewid=10
dronelen=10
dronearea=droneheifh*dronewid*dronelen
battlesize=100000
batarea=battlesize**3
dronesper=batarea/dronearea
print("drone",dronesper)
plastheat=1
plastdens=1
dronethick=.1
dronehvl=1
dronesensorsize=plastdens*dronethick*dronehvl**2
numguns=100000
gunwatt=10*numguns
dronemelt=1000
droneheatcoeff=0.1
droneheatper=(1/dronesensorsize)*(1/droneheatcoeff)
heatpers=gunwatt*droneheatper
timetokill=dronemelt/heatpers
print("drone dies in ",timetokill)
dronespeed=1000
dronecrosstime=battlesize/dronespeed
droneskilledpertime=dronecrosstime/timetokill
volumeoffall=.5*battlesize**3
dronevol=droneheifh*dronewid*dronelen
dronesperfall=volumeoffall/dronevol
droneskilledpertime*=dronesperfall
dronesperfall**=1/2
print("dronesperfall",dronesperfall)
droneskilledpertime/=dronesper
print("x over drones killed",droneskilledpertime)
print("share droenes killed",droneskilledpertime/dronesperfall)

import math

# Drone and battlefield dimensions
drone_h = 10
drone_w = 10
drone_l = 10
drone_vol = drone_h * drone_w * drone_l

battle_size = 100000
battle_vol = battle_size**3

# Total drones possible
drones_total = battle_vol / drone_vol
print("Total drones:", drones_total)

# Sensor heat properties
plastdens = 1
drone_thick = 0.1
drone_hvl = 1
dronesensor_size = plastdens * drone_thick * drone_hvl**2  # 0.1

# Gun setup
num_guns = 100000
gun_watt = 10 * num_guns

# Thermal kill parameters
drone_melt = 1000
drone_heat_coeff = 0.1
drone_heat_per = (1/dronesensor_size) * (1/drone_heat_coeff)
heat_per_s = gun_watt * drone_heat_per
time_to_kill = drone_melt / heat_per_s
print("Drone dies in", time_to_kill, "seconds")

# Crossing time
drone_speed = 1000
cross_time = battle_size / drone_speed

# Kill rate
kills_possible = cross_time / time_to_kill

# Your original scaling with volume of fall
volume_of_fall = 0.5 * battle_vol
drones_per_fall = volume_of_fall / drone_vol
kills_possible *= drones_per_fall

# Extra square-root adjustment (your fudge factor)
drones_per_fall = drones_per_fall**0.5

# Normalize by total drones
kills_effective = kills_possible / drones_total

# Survivors
survival_share = max(0, 1 - kills_effective)
surviving_drones = drones_total * survival_share

print("Effective kills factor:", kills_effective)
print("Absolute surviving drones:", surviving_drones)
print("Survival percent:", (surviving_drones/drones_total)*100, "%")