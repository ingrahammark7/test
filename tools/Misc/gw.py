import random
import time

# ==========================
# Fighter class
# ==========================
class Fighter:
    def __init__(self, name, health, stamina, attack, defense, speed, special_moves):
        self.name = name
        self.max_health = health
        self.health = health
        self.stamina = stamina
        self.max_stamina = stamina
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.special_moves = special_moves
        self.status_effects = []  # e.g., 'stun', 'poison', 'burn'

    def is_alive(self):
        return self.health > 0

    def apply_status_effects(self):
        for effect in self.status_effects[:]:
            if effect == "poison":
                damage = max(1, self.max_health // 20)
                self.health -= damage
                print(f"{self.name} suffers {damage} poison damage!")
            elif effect == "burn":
                damage = max(1, self.max_health // 15)
                self.health -= damage
                print(f"{self.name} suffers {damage} burn damage!")
            elif effect == "stun":
                print(f"{self.name} is stunned and may miss their turn!")
            # Remove temporary effects if needed
            if random.random() < 0.2:  # 20% chance to remove effect each turn
                print(f"{self.name} is no longer affected by {effect}.")
                self.status_effects.remove(effect)

    def take_damage(self, damage):
        mitigated = max(0, damage - self.defense)
        self.health -= mitigated
        print(f"{self.name} takes {mitigated} damage (after defense).")

    def perform_attack(self, target, move):
        hit_chance = 0.8 + (self.speed - target.speed) * 0.01
        if random.random() > hit_chance:
            print(f"{self.name}'s {move['name']} missed!")
            return
        base_damage = move['power'] + self.attack
        if 'status' in move:
            if random.random() < move.get('status_chance', 0.3):
                target.status_effects.append(move['status'])
                print(f"{target.name} is now {move['status']}!")
        crit = 1.5 if random.random() < 0.1 else 1.0
        total_damage = int(base_damage * crit)
        if crit > 1:
            print("Critical hit!")
        target.take_damage(total_damage)
        self.stamina -= move.get('stamina_cost', 0)

# ==========================
# Predefined fighters
# ==========================
fighters = [
    Fighter("Warrior", 120, 50, 15, 5, 10, [
        {"name": "Power Strike", "power": 25, "stamina_cost": 10},
        {"name": "Stunning Blow", "power": 10, "stamina_cost": 8, "status": "stun", "status_chance": 0.5}
    ]),
    Fighter("Mage", 80, 100, 10, 3, 12, [
        {"name": "Fireball", "power": 20, "stamina_cost": 15, "status": "burn", "status_chance": 0.5},
        {"name": "Ice Shard", "power": 15, "stamina_cost": 10, "status": "stun", "status_chance": 0.3}
    ]),
    Fighter("Rogue", 100, 60, 12, 4, 18, [
        {"name": "Backstab", "power": 20, "stamina_cost": 8},
        {"name": "Poison Dagger", "power": 10, "stamina_cost": 5, "status": "poison", "status_chance": 0.6}
    ])
]

# ==========================
# Utility Functions
# ==========================
def choose_fighter():
    print("Choose your fighter:")
    for idx, f in enumerate(fighters):
        print(f"{idx + 1}: {f.name} (HP: {f.health}, Stamina: {f.stamina}, Atk: {f.attack}, Def: {f.defense}, Spd: {f.speed})")
    choice = int(input("Enter number: ")) - 1
    return fighters[choice]

def choose_move(fighter):
    print(f"Choose move for {fighter.name}:")
    for idx, move in enumerate(fighter.special_moves):
        print(f"{idx + 1}: {move['name']} (Power: {move['power']}, Stamina Cost: {move.get('stamina_cost', 0)})")
    choice = int(input("Enter number: ")) - 1
    return fighter.special_moves[choice]

def ai_choose_move(fighter):
    available_moves = [m for m in fighter.special_moves if fighter.stamina >= m.get('stamina_cost', 0)]
    return random.choice(available_moves)

# ==========================
# Game loop
# ==========================
def battle(player, enemy):
    print(f"\nBattle Start: {player.name} vs {enemy.name}!\n")
    turn = 0
    while player.is_alive() and enemy.is_alive():
        turn += 1
        print(f"\n--- Turn {turn} ---")
        # Apply status effects
        player.apply_status_effects()
        enemy.apply_status_effects()

        # Player's turn
        move = choose_move(player)
        player.perform_attack(enemy, move)
        if not enemy.is_alive():
            print(f"{enemy.name} is defeated! You win!")
            break

        # Enemy's turn
        move = ai_choose_move(enemy)
        print(f"{enemy.name} uses {move['name']}!")
        enemy.perform_attack(player, move)
        if not player.is_alive():
            print(f"{player.name} is defeated! Game Over!")
            break

        # Display health and stamina
        print(f"\nStatus:\n{player.name} - HP: {player.health}/{player.max_health}, Stamina: {player.stamina}/{player.max_stamina}")
        print(f"{enemy.name} - HP: {enemy.health}/{enemy.max_health}, Stamina: {enemy.stamina}/{enemy.max_stamina}")

# ==========================
# Main
# ==========================
if __name__ == "__main__":
    player = choose_fighter()
    enemy = random.choice([f for f in fighters if f != player])
    battle(player, enemy)