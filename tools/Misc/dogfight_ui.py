import tkinter as tk
from tkinter import ttk
import threading
import matplotlib.pyplot as plt

from fight import DogfightSimulator, fighters  # Import from your existing file

class DogfightApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Dogfight Simulator")

        # Fighter selection
        self.fighters_list = list(fighters.keys())

        ttk.Label(root, text="Select Fighter 1:").grid(row=0, column=0, padx=5, pady=5)
        self.fighter1_var = tk.StringVar(value=self.fighters_list[0])
        self.fighter1_combo = ttk.Combobox(root, textvariable=self.fighter1_var, values=self.fighters_list, state="readonly")
        self.fighter1_combo.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Select Fighter 2:").grid(row=1, column=0, padx=5, pady=5)
        self.fighter2_var = tk.StringVar(value=self.fighters_list[1])
        self.fighter2_combo = ttk.Combobox(root, textvariable=self.fighter2_var, values=self.fighters_list, state="readonly")
        self.fighter2_combo.grid(row=1, column=1, padx=5, pady=5)

        # Start Button
        self.start_button = ttk.Button(root, text="Start Simulation", command=self.start_simulation)
        self.start_button.grid(row=2, column=0, columnspan=2, pady=10)

        # Flag to track if sim is running
        self.sim_running = False

    def start_simulation(self):
        if self.sim_running:
            return  # Already running
        self.sim_running = True

        # Disable controls during simulation
        self.start_button.config(state=tk.DISABLED)
        self.fighter1_combo.config(state=tk.DISABLED)
        self.fighter2_combo.config(state=tk.DISABLED)

        # Run simulation in separate thread to keep UI responsive
        threading.Thread(target=self.run_simulation).start()

    def run_simulation(self):
        ac1 = self.fighter1_var.get()
        ac2 = self.fighter2_var.get()

        sim = DogfightSimulator(ac1, ac2)
        plt.show()

        # When plt window closes, re-enable controls
        self.root.after(0, self.reset_ui)

    def reset_ui(self):
        self.sim_running = False
        self.start_button.config(state=tk.NORMAL)
        self.fighter1_combo.config(state=tk.NORMAL)
        self.fighter2_combo.config(state=tk.NORMAL)

if __name__ == "__main__":
    root = tk.Tk()
    app = DogfightApp(root)
    root.mainloop()