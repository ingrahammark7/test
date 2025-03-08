import tkinter as tk
import random

# Map dimensions
MAP_WIDTH = 7
MAP_HEIGHT = 7

class TacticalMap:
    def __init__(self, root):
        self.root = root
        self.map = {}
        self.turn = "Player"  # Alternates between "Player" and "Enemy"
        self.player_unit = {"name": "T-64 Tank", "hp": 20, "ammo": 5}  # Player stats
        self.enemy_unit = {"name": "Enemy Unit", "hp": 10}
        self.player_position = "A1"  # Track player's current position
        self.enemy_count = 5  # Total number of enemies
        self.score = 0  # Player's score
        self.log = []  # Combat log
        self.create_map()
        self.deploy_units()
        self.create_log_area()

    def create_map(self):
        self.frame = tk.Frame(self.root)
        self.frame.pack()
        for row in range(MAP_HEIGHT):
            for col in range(MAP_WIDTH):
                coord = f"{chr(65 + row)}{col + 1}"  # Coordinates (e.g., A1, B2)
                button = tk.Button(
                    self.frame,
                    text="Empty",
                    width=10,
                    height=3,
                    command=lambda c=coord: self.on_cell_click(c)
                )
                button.grid(row=row, column=col)
                self.map[coord] = button

    def create_log_area(self):
        # Create a text area to display combat logs
        self.log_area = tk.Text(self.root, height=10, width=70)
        self.log_area.pack()
        self.update_log("Game started. Player's turn.")

    def update_log(self, message):
        self.log.append(message)
        self.log_area.insert(tk.END, message + "\n")
        self.log_area.see(tk.END)  # Scroll to the latest log entry

    def deploy_units(self):
        # Place player unit
        self.map[self.player_position].config(text=self.player_unit["name"], bg="blue")

        # Place enemies randomly
        for _ in range(self.enemy_count):
            empty_cells = [coord for coord, button in self.map.items() if button.cget("text") == "Empty"]
            if empty_cells:
                enemy_position = random.choice(empty_cells)
                self.map[enemy_position].config(text=self.enemy_unit["name"], bg="red")

    def on_cell_click(self, coord):
        if self.turn == "Player":  # Player's turn
            self.handle_player_action(coord)

    def handle_player_action(self, coord):
        # Ensure the selected cell is within one tile's distance, including diagonals
        distance_row = abs(ord(coord[0]) - ord(self.player_position[0]))
        distance_col = abs(int(coord[1]) - int(self.player_position[1]))
        if max(distance_row, distance_col) == 1:  # Adjacent (vertical, horizontal, or diagonal)
            if self.map[coord].cget("text") == "Empty":
                # Move the player unit
                self.map[coord].config(text=self.player_unit["name"], bg="blue")
                self.map[self.player_position].config(text="Empty", bg="lightgray")
                self.update_log(f"{self.player_unit['name']} moved from {self.player_position} to {coord}.")
                self.player_position = coord  # Update player's position
                self.end_turn()
            elif self.map[coord].cget("text") == self.enemy_unit["name"]:
                # Attack an enemy unit
                self.attack_enemy(coord)
        else:
            self.update_log("Out of range! Choose a cell within one tile, including diagonals.")

    def attack_enemy(self, enemy_position):
        # Reduce enemy HP
        self.enemy_unit["hp"] -= 10
        if self.enemy_unit["hp"] <= 0:
            self.map[enemy_position].config(text="Destroyed", bg="black")
            self.update_log(f"{self.player_unit['name']} attacked and destroyed {self.enemy_unit['name']} at {enemy_position}.")
            self.score += 10  # Add score for destroying an enemy
            self.enemy_count -= 1  # Reduce remaining enemy count
            if self.enemy_count == 0:
                self.update_log(f"All enemies defeated! You win! Final score: {self.score}")
                self.end_game(victory=True)
        else:
            self.update_log(f"{self.player_unit['name']} attacked {self.enemy_unit['name']} at {enemy_position}. Enemy HP: {self.enemy_unit['hp']}.")
        self.end_turn()

    def enemy_action(self):
        # Enemy takes actions (move or attack)
        enemy_positions = [c for c, button in self.map.items() if button.cget("text") == self.enemy_unit["name"]]
        if enemy_positions:
            for enemy_pos in enemy_positions:
                # Check if the player unit is within attack range (including diagonals)
                distance_row = abs(ord(self.player_position[0]) - ord(enemy_pos[0]))
                distance_col = abs(int(self.player_position[1]) - int(enemy_pos[1]))
                if max(distance_row, distance_col) == 1:  # Adjacent
                    # Enemy attacks the player
                    self.player_unit["hp"] -= 5
                    self.update_log(f"{self.enemy_unit['name']} at {enemy_pos} attacked the {self.player_unit['name']}! Player HP: {self.player_unit['hp']}.")
                    if self.player_unit["hp"] <= 0:
                        self.update_log(f"{self.player_unit['name']} was destroyed! Game over. Final score: {self.score}")
                        self.end_game(victory=False)
                        return  # Stop further enemy actions if the game is over
                else:
                    # Enemy moves if not in attack range
                    empty_cells = [coord for coord, button in self.map.items() if button.cget("text") == "Empty"]
                    if empty_cells:
                        new_position = random.choice(empty_cells)
                        self.map[new_position].config(text=self.enemy_unit["name"], bg="red")
                        self.map[enemy_pos].config(text="Empty", bg="lightgray")
                        self.update_log(f"{self.enemy_unit['name']} moved from {enemy_pos} to {new_position}.")
        self.end_turn()

    def end_turn(self):
        # Switch turns
        if self.turn == "Player":
            self.turn = "Enemy"
            self.update_log("Enemy's turn...")
            self.enemy_action()
        else:
            self.turn = "Player"
            self.update_log("Player's turn...")

    def end_game(self, victory):
        # Disable all buttons to end the game
        for button in self.map.values():
            button.config(state="disabled")
        # Show end screen
        end_message = "You Win!" if victory else "You Died"
        end_message += f"\nFinal Score: {self.score}"
        self.show_end_screen(end_message)

    def show_end_screen(self, message):
        # Create a new popup window for the end screen
        end_screen = tk.Toplevel(self.root)
        end_screen.title("Game Over")
        label = tk.Label(end_screen, text=message, font=("Arial", 16))
        label.pack(pady=20)
        close_button = tk.Button(end_screen, text="Close", command=self.root.destroy)
        close_button.pack(pady=10)

# Initialize GUI
root = tk.Tk()
root.title("Turn-Based Tactical Simulation with Bug Fixes")
game = TacticalMap(root)
root.mainloop()
