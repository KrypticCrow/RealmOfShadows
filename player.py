# player.py
import json
import os

class Player:
    def __init__(self, name):
        self.name = name
        self.hp = 100
        self.max_hp = 100
        self.base_attack = 10
        self.base_defense = 5

        # Equipment
        self.weapon = None
        self.armor = None
        self.inventory = []

        # XP and Level
        self.level = 1
        self.xp = 0

    # ----- STATS -----
    @property
    def attack(self):
        bonus = self.weapon["attack_bonus"] if self.weapon else 0
        return self.base_attack + bonus

    @property
    def defense(self):
        bonus = self.armor["defense_bonus"] if self.armor else 0
        return self.base_defense + bonus

    def is_alive(self):
        return self.hp > 0

    def show_stats(self):
        print("\n=== PLAYER STATS ===")
        print(f"Name: {self.name}")
        print(f"Level: {self.level}")
        print(f"XP: {self.xp}/{self.xp_to_next_level()}")
        print(f"HP: {self.hp}/{self.max_hp}")
        print(f"Attack: {self.attack}")
        print(f"Defense: {self.defense}")
        print(f"Weapon: {self.weapon['name'] if self.weapon else 'None'}")
        print(f"Armor: {self.armor['name'] if self.armor else 'None'}")
        inv_list = [f"{item['name']} x{item.get('quantity',1)}" for item in self.inventory]
        print(f"Inventory: {', '.join(inv_list) if inv_list else 'Empty'}\n")

    # ----- XP / LEVEL -----
    def xp_to_next_level(self):
        return self.level * 100 + (self.level - 1) * 100

    def gain_xp(self, amount):
        print(f"You gained {amount} XP!")
        self.xp += amount
        while self.xp >= self.xp_to_next_level():
            self.xp -= self.xp_to_next_level()
            self.level_up()

    def level_up(self):
        self.level += 1
        self.max_hp += 10
        self.hp = self.max_hp
        self.base_attack += 2
        self.base_defense += 1
        print(f"🎉 Congratulations! You reached Level {self.level}!")
        print("Stats increased: HP +10, Attack +2, Defense +1\n")

    # ----- INVENTORY / EQUIP -----
    def add_item(self, item):
        """Add an item to inventory. Stack duplicates automatically and show level requirement."""
        # Check if item already exists
        for inv_item in self.inventory:
            if inv_item["name"] == item["name"]:
                inv_item["quantity"] = inv_item.get("quantity",1) + 1
                print(f"You obtained another {item['name']}! You now have x{inv_item['quantity']} "
                      f"(Level {item['level_required']} required to equip)")
                return
        # First time obtaining the item
        item["quantity"] = 1
        self.inventory.append(item)
        print(f"You obtained {item['name']}! (Level {item['level_required']} required to equip)")

    def show_inventory(self):
        if not self.inventory:
            print("Inventory is empty.")
            return

        print("\n=== INVENTORY ===")
        for i, item in enumerate(self.inventory, 1):
            qty = f"x{item.get('quantity',1)}" if item.get("quantity",1) > 1 else ""
            print(f"{i}. {item['name']} {qty} (Type: {item['type']}, "
                  f"Lvl Req: {item['level_required']}, "
                  f"ATK: {item.get('attack_bonus',0)}, DEF: {item.get('defense_bonus',0)})")

        choice = input("Enter the number of an item to equip it, or press Enter to exit: ").strip()
        if choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(self.inventory):
                item = self.inventory[idx]
                if self.level >= item["level_required"]:
                    if item["type"] == "weapon":
                        self.weapon = item
                        print(f"You equipped {item['name']} as your weapon.")
                    elif item["type"] == "armor":
                        self.armor = item
                        print(f"You equipped {item['name']} as your armor.")
                else:
                    print(f"You need to be level {item['level_required']} to equip this item.")

    # ----- SAVE / LOAD -----
    def save(self, filename="save.json"):
        data = {
            "name": self.name,
            "hp": self.hp,
            "max_hp": self.max_hp,
            "base_attack": self.base_attack,
            "base_defense": self.base_defense,
            "weapon": self.weapon,
            "armor": self.armor,
            "inventory": self.inventory,
            "level": self.level,
            "xp": self.xp
        }
        with open(filename, "w") as f:
            json.dump(data, f)
        print("Game saved!")

    @classmethod
    def load(cls, filename="save.json"):
        if not os.path.exists(filename):
            return None
        with open(filename, "r") as f:
            data = json.load(f)
        player = cls(data["name"])
        player.hp = data.get("hp", 100)
        player.max_hp = data.get("max_hp", 100)
        player.base_attack = data.get("base_attack", 10)
        player.base_defense = data.get("base_defense", 5)
        player.weapon = data.get("weapon")
        player.armor = data.get("armor")
        player.level = data.get("level", 1)
        player.xp = data.get("xp", 0)

        # ----- MERGE DUPLICATE ITEMS IN INVENTORY -----
        raw_inventory = data.get("inventory", [])
        inventory_dict = {}
        for item in raw_inventory:
            name = item["name"]
            qty = item.get("quantity", 1)
            if name in inventory_dict:
                inventory_dict[name]["quantity"] += qty
            else:
                inventory_dict[name] = item.copy()
                inventory_dict[name]["quantity"] = qty
        player.inventory = list(inventory_dict.values())

        return player
