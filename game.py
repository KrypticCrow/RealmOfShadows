# game.py
import random
from player import Player
from utils import divider, prompt_choice
from enemy import Enemy

class Game:
    def __init__(self):
        self.player = None
        self.running = True

    def start(self):
        divider()
        print("🗡️ Welcome to the Realm of Shadows 🗡️")
        divider()

        existing_player = Player.load()
        if existing_player:
            choice = input("Save file found. Load previous game? (y/n): ").lower()
            if choice == "y":
                self.player = existing_player
                print(f"\nWelcome back, {self.player.name}!\n")
            else:
                name = input("What is your name, adventurer? ")
                self.player = Player(name)
        else:
            name = input("What is your name, adventurer? ")
            self.player = Player(name)

        self.main_loop()

    def main_loop(self):
        while self.running and self.player.is_alive():
            divider()
            print("You stand at a crossroads.")
            options = {
                "1": "Check stats",
                "2": "Explore the forest",
                "3": "Show inventory / Equip",
                "4": "Save game",
                "5": "Quit game"
            }

            choice = prompt_choice(options)

            if choice == "1":
                self.player.show_stats()
            elif choice == "2":
                self.explore_forest()
            elif choice == "3":
                self.player.show_inventory()
            elif choice == "4":
                self.player.save()
                print("Game saved! You can continue your adventure.")
            elif choice == "5":
                print("You lay down your sword. Farewell.")
                self.player.save()
                self.running = False
            else:
                print("Invalid choice.")

    def explore_forest(self):
        divider()
        print("🌲 You venture into the dark forest...")

        encounter_chance = random.randint(1, 100)
        if encounter_chance <= 60:
            enemy = self.generate_random_enemy()
            print(f"A wild {enemy.name} appears!")
            self.combat(enemy)
        else:
            print("The forest is quiet. Nothing attacks you.")

    def generate_random_enemy(self):
        enemies = [
            Enemy("Goblin", hp=30, attack=5, defense=2),
            Enemy("Wolf", hp=25, attack=7, defense=1),
            Enemy("Bandit", hp=35, attack=6, defense=3)
        ]
        return random.choice(enemies)

    def combat(self, enemy):
        while enemy.is_alive() and self.player.is_alive():
            divider()
            print(f"{enemy.name} HP: {enemy.hp}/{enemy.max_hp}")
            print(f"Your HP: {self.player.hp}/{self.player.max_hp}")
            options = {"1": "Attack", "2": "Run"}
            choice = prompt_choice(options)

            if choice == "1":
                # Player attack
                if random.randint(1, 100) <= 10:
                    print("You missed your attack!")
                    damage = 0
                else:
                    damage = max(self.player.attack - enemy.defense, 0)
                    if random.randint(1, 100) <= 10:
                        damage *= 2
                        print("Critical hit!")
                enemy.take_damage(damage)
                if damage > 0:
                    print(f"You strike the {enemy.name} for {damage} damage!")

                # Enemy attack always prints
                if enemy.is_alive():
                    if random.randint(1, 100) <= 10:
                        print(f"{enemy.name} missed!")
                        enemy_damage = 0
                    else:
                        enemy_damage = max(enemy.attack - self.player.defense, 0)
                        if random.randint(1, 100) <= 10:
                            enemy_damage *= 2
                            print(f"{enemy.name} lands a critical hit!")
                    self.player.hp -= enemy_damage
                    print(f"{enemy.name} attacks you for {enemy_damage} damage!")

            elif choice == "2":
                print("You flee back to safety!")
                return
            else:
                print("Invalid choice.")

        if self.player.is_alive() and not enemy.is_alive():
            print(f"You have defeated the {enemy.name}!")
            xp_gain = enemy.max_hp + enemy.attack * 2
            self.player.gain_xp(xp_gain)
            self.generate_loot(enemy)
        elif not self.player.is_alive():
            print("You have been defeated! Game over.")
            self.player.hp = 1
            self.running = False

    # ----- LOOT SYSTEM -----
    def generate_loot(self, enemy):
        loot_table = [
            {"name": "Iron Sword", "type": "weapon", "attack_bonus": 5, "defense_bonus": 0, "level_required": 2},
            {"name": "Steel Sword", "type": "weapon", "attack_bonus": 8, "defense_bonus": 0, "level_required": 3},
            {"name": "Leather Armor", "type": "armor", "attack_bonus": 0, "defense_bonus": 3, "level_required": 1},
            {"name": "Chainmail Armor", "type": "armor", "attack_bonus": 0, "defense_bonus": 5, "level_required": 3},
        ]
        drop_chance = random.randint(1, 100)
        if drop_chance <= 50:
            item = random.choice(loot_table)
            self.player.add_item(item)
