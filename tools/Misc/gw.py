from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.slider import Slider
from kivy.uix.label import Label
from kivy.clock import Clock

import numpy as np

# ============================================================
# SIMPLE PHYSICS CORE (Pydroid-safe)
# ============================================================

def rho(h):
    return 1.225 * np.exp(-h / 8500)

def a_sound():
    return 340.0

A = 0.015
C_th = 900.0
T_MAX = 450.0

def Q_aero(M):
    v = M * a_sound()
    return 2e-4 * rho(5000) * v**3 * A

def Q_elec(P):
    return 50.0 + 0.32 * P

def Q_cool(T):
    return 60.0 * A * (T - 220.0)

# ============================================================
# UI APP
# ============================================================

class ThermalUI(App):

    def build(self):

        self.T = 300.0

        layout = BoxLayout(orientation='vertical')

        # Labels
        self.label_M = Label(text="Mach: 1.0")
        self.label_P = Label(text="Power: 500 W")
        self.label_T = Label(text="Temp: 300 K")
        self.label_status = Label(text="STATUS: STABLE")

        # Sliders
        self.slider_M = Slider(min=0.5, max=6.0, value=1.0)
        self.slider_P = Slider(min=0, max=2000, value=500)

        self.slider_M.bind(value=self.update)
        self.slider_P.bind(value=self.update)

        layout.add_widget(self.label_M)
        layout.add_widget(self.slider_M)

        layout.add_widget(self.label_P)
        layout.add_widget(self.slider_P)

        layout.add_widget(self.label_T)
        layout.add_widget(self.label_status)

        # simulation loop
        Clock.schedule_interval(self.step, 0.1)

        return layout

    # ========================================================
    # REAL-TIME UPDATE
    # ========================================================

    def update(self, instance, value):
        self.label_M.text = f"Mach: {self.slider_M.value:.2f}"
        self.label_P.text = f"Power: {self.slider_P.value:.0f} W"

    # ========================================================
    # TIME EVOLUTION
    # ========================================================

    def step(self, dt):

        M = self.slider_M.value
        P = self.slider_P.value

        Qin = Q_aero(M) + Q_elec(P)
        Qout = Q_cool(self.T)

        dT = (Qin - Qout) / C_th

        self.T += dT * 0.1

        self.label_T.text = f"Temp: {self.T:.1f} K"

        if self.T > T_MAX:
            self.label_status.text = "STATUS: OVERHEAT"
        else:
            self.label_status.text = "STATUS: STABLE"


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    ThermalUI().run()