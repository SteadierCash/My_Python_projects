import random
import json


class Spell:
    class_counter = 0

    def __init__(self):
        self.id = Spell.class_counter
        self.name = None
        self.power = None
        self.strength = None
        self.heal = None
        self.kill = None
        self.disappear = None

        self.create_spell()

    def create_spell(self):
        Spell.class_counter += 1
        with open("text_files/spell.json", "r") as file:
            spells = json.load(file)

        spell = random.choice(spells)

        self.name = spell["spell_name"]
        self.power = spell["power"]
        self.strength = spell["strength"]
        self.heal = spell["heal"]
        self.kill = spell["kill"]
        self.disappear = spell["disappear"]

    def show_spell(self):
        s = f"{self.id}. {self.name} - "

        if self.power != 0:
            s += f" Power +{self.power}"

        elif self.strength != 0:
            s += f" Strength +{self.strength}"

        elif self.heal != 0:
            s += f" You can be healed"

        elif self.kill != 0:
            s += f" You can instantly kill an enemy"

        elif self.disappear != 0:
            s += f" You can disappear and run from an enemy"

        return s

    def to_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "power": self.power,
            "strength": self.strength,
            "heal": self.heal,
            "kill": self.kill,
            "disappear": self.disappear
        }
