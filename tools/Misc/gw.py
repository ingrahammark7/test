import numpy as np
import matplotlib.pyplot as plt

# physical constants
rho = 1.225  # air density kg/m^3
CdA = 0.65   # typical sedan
P_max = 112000  # 150 hp in watts

# power loss range
loss = np.linspace(0, 0.9, 200)
P = P_max * (1 - loss)

# max speed from drag equation
v = ((2 * P) / (rho * CdA)) ** (1/3)

# convert to km/h
v_kmh = v * 3.6

plt.plot(loss * 100, v_kmh)
plt.xlabel("Power loss (%)")
plt.ylabel("Max speed (km/h)")
plt.title("Real Car Max Speed vs Power Loss (Physics-based)")
plt.grid(True)
plt.show()

# print key values
print("No loss max speed:", v_kmh[0], "km/h")
print("50% loss max speed:", v_kmh[100], "km/h")
print("80% loss max speed:", v_kmh[160], "km/h")