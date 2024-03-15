import random
import json


class Weapon:
    class_counter = 0
    
    def __init__(self):
        self.id = Weapon.class_counter
        self.name = None
        self.power = None
        self.strength = None

        self.create_weapon()

    def create_weapon(self):
        Weapon.class_counter += 1

        with open("text_files/weapons.json", "r") as file:
            weapons = json.load(file)

        weapon = random.choice(weapons)

        self.name = weapon["weapon_name"]
        self.power = weapon["power"]
        self.strength = weapon["strength"]

    def show_weapon(self):
        s = f"{self.id}. {self.name}"

        if self.power != 0:
            s += f" Power +{self.power}"

        if self.strength != 0:
            s += f" Strength +{self.strength}"

        return s

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "power": self.power,
            "strength": self.strength
        }
