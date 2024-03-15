import random
import json


def stat(enemy, hero):
    n = random.randint(-3, 5)
    return max(0, enemy * (hero + n))


def choose_enemy():
    with open("text_files/fight.json", "r") as file:
        events = json.load(file)

    return random.choice(events)


class Enemy:
    def __init__(self, name, hero_power, hero_strength, power, strength):
        self.name = name
        self.power = stat(power, hero_power)
        self.strength = stat(strength, hero_strength)
        self.attack = 0
        self.coins = self.coins()

    def coins(self):
        n = random.randint(1, 20)
        return n * max(self.power, self.strength)

    def __repr__(self):
        s = f"You Figth with {self.name}"

        if self.power != 0:
            s += f" Power: {self.power}"
        else:
            s += f" Strength: {self.strength}"

        s += f" Defending: {self.coins} coins"

        return s