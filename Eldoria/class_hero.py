import random
import json


class Hero:
    def __init__(self):
        self.name = None
        self.power = None
        self.strength = None
        self.lives = None
        self.max_lives = None
        self.coins = 100
        self.attack = 0
        self.spells = []
        self.weapons = []

        # self.choose_character("heroes.json")

    def show_hero_weapons(self):
        s = ""
        if self.weapons:
            s += f"\nWeapons: ["
            for weapon in self.weapons:
                s += weapon.show_weapon()
                s += ", "
            s += "]"

        return s

    def show_hero_spells(self):
        s = ""
        if self.spells:
            s += f"\nSpells: ["
            for spell in self.spells:
                s += spell.show_spell()
                s += ", "
            s += "]"

        return s

    def choose_character(self, char_file):
        with open("text_files/" + char_file, "r") as file:
            char = json.load(file)

        if char_file == "heroes.json":
            print("Choose your character by selecting his id: ")
            print("")
            for character in char:
                print(f"Character ID: {character['character_id']} ", end="")
                print(f"Class: {character['class']} ", end="")
                print(f"Power: {character['power']} ", end="")
                print(f"Strength: {character['strength']} ", end="")
                print(f"Lives: {character['lives']} ")

                print("---------------------")

            c_id = -1

            print("")
            while int(c_id) < 1 or int(c_id) > len(char):
                c_id = int(input("$ ID: "))
                print("")

        else:
            c_id = str(random.randint(1, len(char)))

        for character in char:
            if character['character_id'] == c_id:
                self.name = character['class']
                self.power = character['power']
                self.strength = character['strength']
                self.lives = character['lives']
                self.max_lives = character['lives']
                break

    def __repr__(self):
        s = (f"Your Character stats:"
             f"\nName: {self.name}"
             f"\nPower: {self.power}"
             f"\nStrength: {self.strength}"
             f"\nLives: {self.lives}"
             f"\nCoins: {self.coins}")

        s += self.show_hero_spells()
        s += self.show_hero_weapons()

        return s

    def to_json(self):
        spells_json = [spell.to_json() for spell in self.spells]
        weapons_json = [weapon.to_json() for weapon in self.weapons]

        return {
            "name": self.name,
            "power": self.power,
            "strength": self.strength,
            "lives": self.lives,
            "max_lives": self.max_lives,
            "coins": self.coins,
            "attack": self.attack,
            "spells": spells_json,
            "weapons": weapons_json
        }
