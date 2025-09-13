import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider, IntSlider
from matplotlib.collections import LineCollection

# Base parameters
m_shell_base = 5.0       # kg for 1 m shell
A_shell_base = 0.16      # m^2 for 1 m shell
E_max_base = 5e6         # J for 1 m shell
L_barrel = 6.0           # max barrel length (m)
N = 1000                 # simulation segments

dx = L_barrel / N
x = np.linspace(0, L_barrel, N)

def full_barrel_sim(fraction=0.99, h_eff=25, T_gas=1000, num_shells=3,
                    T_mp_min=1200, T_mp_max=3000,
                    c_min=0.4e3, c_max=1.2e3,
                    double_factor=2.0,
                    d_shell=0.10, t_wall=0.01, rho_steel=7850,
                    thermal_fraction=0.9):

    L_shells = np.linspace(0.5, 2.0, num_shells)
    T_mp_array = np.linspace(T_mp_min, T_mp_max, num_shells)
    c_array = np.linspace(c_min, c_max, num_shells)

    fig, axes = plt.subplots(2,4, figsize=(32,12))
    axes = axes.flatten()

    for i, L_shell in enumerate(L_shells):
        m_shell = m_shell_base * L_shell
        A_shell = A_shell_base * L_shell
        E_max = E_max_base * L_shell
        c_shell = c_array[i]
        T_mp = T_mp_array[i]

        # Initialize arrays
        E_deposited = np.zeros(N)
        v_shell = np.zeros(N)
        Q_heat = np.zeros(N)
        T_shell = np.zeros(N)
        Q_dot = h_eff * A_shell * min(T_gas, T_mp)
        efficiency = 0.7

        E_acc = 0
        v_current = 0
        Q_cumulative = 0

        energy_limit = None
        thermal_limit = None
        structural_limit = None

        for j in range(N):
            Q_eff = Q_dot * (L_shell / max(v_current, 0.1))
            dE = Q_eff * dx / L_shell * efficiency
            dE = min(dE, E_max - E_acc)
            E_acc += dE
            E_deposited[j] = E_acc

            dQ = Q_dot * dx / max(v_current, 0.1)
            Q_cumulative += dQ
            Q_heat[j] = Q_cumulative
            T_shell[j] = Q_cumulative / (m_shell * c_shell)
            v_current = np.sqrt(2 * E_acc / m_shell)
            v_shell[j] = v_current

            # Energy limit
            if energy_limit is None and E_acc >= fraction * E_max:
                energy_limit = x[j]

            # Thermal limit
            if thermal_limit is None and T_shell[j] >= thermal_fraction * T_mp:
                thermal_limit = x[j]

            # Structural limit
            m_wall_extra = np.pi * (((d_shell/2 + t_wall)**2 - (d_shell/2)**2) * dx * rho_steel)
            m_prop_equiv = 2 * dE / v_shell[j]**2
            if structural_limit is None and m_wall_extra >= m_prop_equiv:
                structural_limit = x[j]

        # Safe max barrel
        limits = [l for l in [energy_limit, thermal_limit, structural_limit] if l is not None]
        safe_length = min(limits) if limits else L_barrel

        # Double barrel effect
        L_double = safe_length * double_factor
        extra_length = L_double - safe_length
        extra_E = dE * N * (extra_length / L_barrel) * efficiency
        v_double = np.sqrt(2 * (E_deposited[-1] + extra_E) / m_shell)

        # Diminishing returns % per meter
        dv_dx = np.diff(v_shell)/dx
        dv_pct = 100*dv_dx/v_shell[1:]

        # Percent of max velocity
        v_max = np.sqrt(2 * E_max / m_shell)
        v_percent = 100*v_shell/v_max

        # ---- Plots ----
        # 1. Velocity
        axes[0].plot(x, v_shell/1000, label=f'Shell {L_shell:.2f} m')
        axes[0].axvline(safe_length, color='red', linestyle='-.', alpha=0.7, label='Safe Max Barrel')

        # 2. Kinetic energy with wasted shading
        axes[1].plot(x, 0.5*m_shell*v_shell**2/1e6)
        axes[1].fill_between(x, 0, 0.5*m_shell*v_shell**2/1e6, where=(x>safe_length), color='grey', alpha=0.3)

        # 3. Heat stress
        points = np.array([x, T_shell]).T.reshape(-1,1,2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        lc = LineCollection(segments, cmap='RdYlGn_r', norm=plt.Normalize(0,1))
        lc.set_array(T_shell/T_mp)
        lc.set_linewidth(2)
        axes[2].add_collection(lc)
        axes[2].plot(x, T_shell, alpha=0)
        axes[2].axhline(T_mp, color='black', linestyle='--', alpha=0.7)
        axes[2].axvline(safe_length, color='red', linestyle='-.', alpha=0.7)

        # 4. Diminishing returns
        axes[3].plot(x[1:], dv_pct)

        # 5. Double barrel effect (velocity)
        axes[4].plot([x[-1], L_double], [v_shell[-1]/1000, v_double/1000], linestyle='--', color='purple')

        # 6. Percent of max velocity
        axes[5].plot(x, v_percent)

        # 7. Combined: KE + safe length + velocity %
        axes[6].plot(x, 0.5*m_shell*v_shell**2/1e6, label=f'Shell {L_shell:.2f} m')
        axes[6].axvline(safe_length, color='red', linestyle='-.')
        axes[6].fill_between(x, 0, 0.5*m_shell*v_shell**2/1e6, where=(x>safe_length), color='grey', alpha=0.3)
        axes[6].plot(x, v_percent*v_max/1e6, linestyle=':', color='green', label='% Max Velocity')

        # Console output
        print(f"Shell {L_shell:.2f} m:")
        print(f"  Energy Limit = {energy_limit:.2f} m")
        print(f"  Thermal Limit = {thermal_limit:.2f} m")
        print(f"  Structural Limit = {structural_limit:.2f} m")
        print(f"  SAFE Maximum Barrel Length = {safe_length:.2f} m")
        print(f"  Max velocity = {v_shell[-1]/1000:.3f} km/s, Double barrel = {v_double/1000:.3f} km/s\n")

    titles = ['Velocity (km/s)','Kinetic Energy (MJ)','Shell Heat Stress','Diminishing Returns (%/m)',
              'Double Barrel Effect','Percent of Max Velocity','KE + Velocity % vs Safe Barrel','']
    for ax, title in zip(axes, titles):
        ax.set_title(title)
        ax.grid(True)
        ax.legend(fontsize=8)

    plt.tight_layout()
    plt.show()


# ---- Interactive sliders ----
interact(full_barrel_sim,
         fraction=FloatSlider(min=0.1,max=1.0,step=0.01,value=0.99,description='Energy Fraction'),
         h_eff=FloatSlider(min=5,max=100,step=1,value=25,description='Heat Coefficient'),
         T_gas=FloatSlider(min=500,max=3000,step=50,value=1000,description='Gas Temp (K)'),
         num_shells=IntSlider(min=2,max=5,step=1,value=3,description='Number of Shells'),
         T_mp_min=FloatSlider(min=1000,max=2500,step=50,value=1200,description='Min Melting Pt K'),
         T_mp_max=FloatSlider(min=2000,max=4000,step=50,value=3000,description='Max Melting Pt K'),
         c_min=FloatSlider(min=0.3e3,max=1.0e3,step=50,value=0.4e3,description='Min c J/kgK'),
         c_max=FloatSlider(min=0.8e3,max=2.0e3,step=50,value=1.2e3,description='Max c J/kgK'),
         double_factor=FloatSlider(min=1.1,max=3.0,step=0.1,value=2.0,description='Double Factor'),
         d_shell=FloatSlider(min=0.05,max=0.3,step=0.01,value=0.10,description='Shell Diameter (m)'),
         t_wall=FloatSlider(min=0.005,max=0.05,step=0.001,value=0.01,description='Barrel Wall (m)'),
         thermal_fraction=FloatSlider(min=0.5,max=1.0,step=0.01,value=0.9,description='Thermal Fraction'));