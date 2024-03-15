import json
import random

from class_path import Path
from class_enemy import Enemy, choose_enemy
from class_hero import Hero
from class_spell import Spell
from class_weapon import Weapon


class Game:
    def __init__(self):
        self.fight_outcome = None
        self.hero = None
        self.enemy = None
        self.event = None
        self.path = None
        self.chapter = 0
        self.strength_cost = 150
        self.power_cost = 150
        self.lives_cost = 150
        self.weapons_cost = 300
        self.spells_cost = 300
        self.chapter_1_decision = None

    def gameplay(self):
        print("Welcome in + Eldoria: Magic Quest +")
        print("")

        print("1. Play the Game")
        print("2. Load the Game")
        print("3. Quit the Game")
        print("")

        c = 0

        while c < 1 or c > 3:
            c = int(input("$ What do you want to do?: "))

        if c == 1:
            self.chapter_0()

        elif c == 2:
            loaded = self.load()
            if loaded == 0:
                print("")
                question = input("$ Do you want to start a new game? (y/n):  ")
                print("")
                if question.lower() in ["y", "yes"]:
                    self.chapter_0()
                else:
                    return 0

        else:
            return 0

        while self.hero.lives > 0:
            print("1. Adventure")
            print("2. See Character")
            print("3. Save")
            print("4. Quit")
            ans = int(input("$ What do you want to do?: "))
            print("")

            if ans < 1 or ans > 4:
                continue

            elif ans == 1:
                self.choose_path()
                self.what_action()

            elif ans == 2:
                print(self.hero)
                print("---------")
                print("")

            elif ans == 3:
                self.save()

            elif ans == 4:
                break

            if self.hero.lives == 0:
                self.death()

    def save(self):
        print("saving....")
        print("game saved!")
        hero_json = self.hero.to_json() if self.hero else None

        name = input("$Write name of save: ")

        data = {
            "save_name": name,
            "hero": hero_json,
            "chapter": self.chapter,
            "strength_cost": self.strength_cost,
            "power_cost": self.power_cost,
            "lives_cost": self.lives_cost,
            "weapons_cost": self.weapons_cost,
            "spells_cost": self.spells_cost,
            "chapter_1_decision": self.chapter_1_decision
        }

        json_object = json.dumps(data, indent=4)

        with open("text_files/save.json", mode='a') as file:
            file.write(json_object)

    def load(self):
        try:
            print("+++ Loading... +++")

            with open("text_files/save.json", mode='r') as file:
                data = json.load(file)

            weapons = []
            for el in data['hero']['weapons']:
                weapon = Weapon()
                weapon.id = el['id']
                weapon.name = el['name']
                weapon.power = el['power']
                weapon.strength = el['strength']

                weapons.append(weapon)

            spells = []
            for el in data['hero']['spells']:
                spell = Spell()
                spell.id = el['id']
                spell.name = el['name']
                spell.power = el['power']
                spell.strength = el['strength']
                spell.heal = el['heal']
                spell.kill = el['kill']
                spell.disappear = el['disappear']

                spells.append(spell)

            hero = Hero()
            hero.name = data['hero']['name']
            hero.power = data['hero']['power']
            hero.strength = data['hero']['strength']
            hero.lives = data['hero']['lives']
            hero.max_lives = data['hero']['max_lives']
            hero.coins = data['hero']['coins']
            hero.attack = data['hero']['attack']
            hero.weapons = weapons
            hero.spells = spells

            self.hero = hero
            self.chapter = data['chapter']
            self.strength_cost = data['strength_cost']
            self.power_cost = data['power_cost']
            self.lives_cost = data['lives_cost']
            self.weapons_cost = data['weapons_cost']
            self.spells_cost = data['spells_cost']
            self.chapter_1_decision = data['chapter_1_decision']

            print(f"+++ Loaded {data['save_name']} file! +++")
            print("")

            return 1

        except FileNotFoundError:
            print("+++ You don't have any saved progress +++")

            return 0

    def choose_hero(self):
        self.hero = Hero()
        self.hero.choose_character("heroes.json")
        print(self.hero)
        print("---------")
        print("")

    def choose_path(self):
        self.path = Path(self.chapter)
        self.path.draw_path()
        self.event = self.path.ask_for_action()

        if self.event['action'] != 'story':
            print(self.event["description"])

    def what_action(self):
        if self.event['action'] == "fight":
            self.fight()
        elif self.event['action'] == "shop":
            self.shop()
        elif self.event['action'] == "friend":
            self.friend()
        elif self.event['action'] == "story":
            self.story()

    def fight(self, is_story=False):
        self.enemy = Enemy(self.event['name_of_enemy'], self.hero.power, self.hero.strength,
                           self.event['power'], self.event['strength'])
        print(self.enemy)
        print("---------")
        print("You have ", end="")
        if self.enemy.power != 0:
            print(f"Power: {self.hero.power}")
        else:
            print(f"Strength: {self.hero.strength}")
        print("")

        while True:
            max_user_action = 2

            print("1. Attack")
            print("2. Use spell")
            if not is_story:
                print("3. Run")
                max_user_action = 3

            print("")

            user_action = -1
            while 1 > user_action or user_action > max_user_action:
                user_action = int(input("$ What do you want to do?: "))

            if user_action == 1:
                if self.attack(is_story) == 1:
                    self.hero.attack = 0
                    self.enemy = None
                    break

            elif user_action == 2:
                if self.use_spell(is_story) == 1:
                    self.hero.attack = 0
                    self.enemy = None
                    break

            elif user_action == 3:
                self.run()
                self.hero.attack = 0
                self.enemy = None
                break

        self.hero.attack = 0
        self.enemy = None

    def outcome(self, is_story):
        if self.enemy.power != 0:
            if self.hero.power + self.hero.attack > self.enemy.power + self.enemy.attack:
                self.hero.coins += self.enemy.coins
                print("+++ You won! +++")
                return 1
            elif not is_story:
                self.hero.lives -= 1
                print("+++ You lost +++")
                return 0

            else:
                return 0
        else:
            if self.hero.strength + self.hero.attack > self.enemy.strength + self.enemy.attack:
                self.hero.coins += self.enemy.coins
                print("+++ You won! +++")
                return 1

            elif not is_story:
                self.hero.lives -= 1
                print("+++ You lost +++")
                return 0

            else:
                return 0

    def attack(self, is_story):
        while True:
            print("1. Hit")
            print("2. Use weapon")
            print("3. Go back")

            print("")

            user_action = 0
            while 1 > user_action or user_action > 3:
                user_action = int(input("What do you want to do?: "))
                print("")

            # Just attack
            if user_action == 1:
                hit = random.randint(1, 6)
                break

            # Use weapon
            elif user_action == 2:
                print(self.hero.show_hero_weapons())
                w = int(input("Which weapon do you want to use?: (write id or -1 to go back) "))

                if w != -1:
                    hit = self.use_weapon(w)
                    hit += random.randint(1, 6)
                    break

            # Go back
            elif user_action == 3:
                return 0

        self.hero.attack = hit
        self.enemy.attack = random.randint(1, 8)
        print(f"Your attack is {hit}")
        print(f"{self.enemy.name} attack is {self.enemy.attack}")

        self.fight_outcome = self.outcome(is_story)

        print("---------")
        print("")

        return 1

    def use_weapon(self, w):
        p = random.randint(1, 10)
        hit = 0

        if p == 5:
            print("+++ Your weapon broke! +++")
            self.hero.weapons.pop(w)

        else:
            if self.enemy.power != 0:
                hit = self.hero.weapons[w].power

            else:
                hit = self.hero.weapons[w].strength

        return hit

    def use_spell(self, is_story=False):
        # 1 means enemy is dead

        print(self.hero.show_hero_spells())
        while True:
            s = int(input("$ Which spell do you want to use?: (write id or -1 to go back) "))
            print("")
            if s == -1:
                return 0
            else:
                break

        if self.hero.spells[s].power != 0:
            self.hero.attack += self.hero.spells[s].power

        elif self.hero.spells[s].strength != 0:
            self.hero.attack += self.hero.spells[s].strength

        elif self.hero.spells[s].heal != 0:
            self.hero.lives = self.hero.max_lives

        elif self.hero.spells[s].kill != 0:
            self.hero.spells.pop(s)
            self.hero.coins += self.enemy.coins
            print(f"+++ Your spell killed {self.enemy.name}! +++")
            print("---------")
            print("")
            return 1

        elif self.hero.spells[s].disappear != 0 and not is_story:
            self.hero.spells.pop(s)
            print("+++ You manage to run away +++")
            print("")
            return 1

        elif self.hero.spells[s].disappear != 0 and is_story:
            print("+++ Some strong force disabled your spell, you can't run away +++")

        self.hero.spells.pop(s)
        return 0

    def run(self):
        p = random.randint(1, 5)
        if p == 3:
            self.hero.lives -= 2
            print(f"+++ {self.enemy.name} hit you in the back. You lost 2 lives +++")
            print("")
        else:
            print("+++ You manage to run away +++")
            print("")

    def upgrade_attribute(self, attr, stat=True, item=None):
        if self.hero.coins > self.strength_cost:
            self.hero.coins -= getattr(self, attr + "_cost")
            if stat:
                setattr(self.hero, attr, getattr(self.hero, attr) + 1)
                print(f"+++ You gained {attr} point! +++")
            else:
                getattr(self.hero, attr).append(item)
                setattr(self.hero, attr, getattr(self.hero, attr))
                if attr == "weapons":
                    print(f"+++ You gained a new weapon! - {item.show_weapon()} +++")
                    print("")
                else:
                    print(f"+++ You gained a new spell! - {item.show_spell()} +++")
                    print("")
            setattr(self, attr + "_cost", round(getattr(self, attr + "_cost") * 1.2, 0))
            return 1
        else:
            print("+++ You do not have enough coins +++")
            print("")
            return 0

    def shop(self):
        weapon1 = Weapon()
        weapon2 = Weapon()
        spell1 = Spell()
        spell2 = Spell()

        while True:

            print("---- SHOP ----")
            print(f"1. Strength +1                                                 - {self.strength_cost} coins")
            print(f"2. Power +1                                                    - {self.power_cost} coins")
            print(f"3. Life +1                                                     - {self.lives_cost} coins")
            if weapon1:
                print(f"4. {weapon1.show_weapon()}" +
                      " " * (60 - len(weapon1.show_weapon())) +
                      f"- {self.weapons_cost} coins")
            if weapon2:
                print(f"5. {weapon2.show_weapon()}" +
                      " " * (60 - len(weapon2.show_weapon())) +
                      f"- {self.weapons_cost} coins")
            if spell1:
                print(f"6. {spell1.show_spell()}" +
                      " " * (60 - len(spell1.show_spell())) +
                      f"- {self.spells_cost} coins")
            if spell2:
                print(f"7. {spell2.show_spell()}" +
                      " " * (60 - len(spell2.show_spell())) +
                      f"- {self.spells_cost} coins")
            print(f"8. EXIT")
            print("")
            ans = int(input("$ What do you want to buy?: "))
            print("")

            if ans == 1:
                self.upgrade_attribute('strength')
            elif ans == 2:
                self.upgrade_attribute('power')
            elif ans == 3:
                self.upgrade_attribute('lives')
            elif ans == 4:
                a = self.upgrade_attribute('weapons', False, weapon1)
                if a == 1:
                    weapon1 = None
            elif ans == 5:
                a = self.upgrade_attribute('weapons', False, weapon2)
                if a == 1:
                    weapon2 = None
            elif ans == 6:
                a = self.upgrade_attribute('spells', False, spell1)
                if a == 1:
                    spell1 = None
            elif ans == 7:
                a = self.upgrade_attribute('spells', False, spell2)
                if a == 1:
                    spell2 = None
            else:
                break

    def friend(self):
        if self.event["bonus"] == "weapon":
            weapon = Weapon()
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print(f"+++ You gained a new weapon! - {weapon.show_weapon()} +++")
                print("")
                self.hero.weapons.append(weapon)

        elif self.event["bonus"] == "spell":
            spell = Spell()
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print(f"+++ You gained a new spell! - {spell.show_spell()} +++")
                print("")
                self.hero.spells.append(spell)

        elif self.event["bonus"] == "heal":
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print("+++ You have been healed! +++")
                self.hero.lives = self.hero.max_lives

        elif self.event["bonus"] == "power":
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print(f"+++ You gained {self.event['power_points']} power points! +++")
                self.hero.power += self.event['power_points']

        elif self.event["bonus"] == "strength":
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print(f"+++ You gained {self.event['strength_points']} strength points! +++")
                self.hero.power += self.event['strength_points']

        elif self.event["bonus"] == "coins":
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print(f"+++ You gained {self.event['coins_amount']} coins! +++")
                self.hero.power += self.event['coins_amount']

    def story(self):
        chapters = [self.chapter_0, self.chapter_1, self.chapter_2, self.chapter_3, self.chapter_4, self.chapter_5]

        return chapters[self.chapter]()

    def chapter_0(self):
        self.print_chapter()
        print("")
        with open("text_files/story.json", "r") as file:
            story = json.load(file)

        print(story["story"][self.chapter]["story"][0])

        self.choose_hero()

        print(story["story"][self.chapter]["story"][1])
        print("")

        dial = story["story"][self.chapter]["dialogues"]

        for d in dial:
            print(d)
            print("")

        self.chapter += 1

    def chapter_1(self):
        self.print_chapter()
        print("")
        with open("text_files/story.json", "r") as file:
            story = json.load(file)

        print(story["story"][self.chapter]["story"])
        print("")
        print(story["story"][self.chapter]["dialogue"])
        print("")

        for el in story["story"][self.chapter]["options"]:
            print(f"{el['id']}. {el['text']}")

        c = int(input("$ What do you want to do?: "))
        print("")

        choice = story["story"][self.chapter]["options"][c - 1]

        print(choice['response'])
        print("")

        self.chapter_1_decision = choice['decision']

        if choice["id"] == 1:
            self.hero.coins += choice['result']
            print("++ You gained 1000 coins ++")
            print("")

            self.chapter_1_decision = "not_help"

        else:
            print(story["story"][self.chapter]["fight_dialogue"]["player"])
            print("")
            print(story["story"][self.chapter]["fight_dialogue"]["assailant"])
            print("")

            self.event = choose_enemy()

            self.fight(is_story=True)

            if self.fight_outcome == 1:
                print(story["story"][self.chapter]["won_dialogue"])

                weapon = Weapon()
                if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                    print("")
                    print(f"+++ You gained a new weapon! - {weapon.show_weapon()} +++")
                    print("")
                    self.hero.weapons.append(weapon)

                self.chapter_1_decision = "help"

            else:
                print(story["story"][self.chapter]["lost_dialogue"])
                self.hero.lives = 0

        print("")

        self.chapter += 1

    def chapter_2(self):
        self.print_chapter()
        with open("text_files/story.json", "r") as file:
            story = json.load(file)

        print(story["story"][self.chapter]["story"][0])
        print("")
        print(story["story"][self.chapter]["story"][1])
        print("")

        if self.chapter_1_decision == "help":

            for el in story["story"][self.chapter]["help_dialogue"]:
                print(el)
                print("")

            self.hero.attack += 5
            print("++ You gained 5 attack points ++")

        elif self.chapter_1_decision == "not_help":

            for el in story["story"][self.chapter]["not_help_dialogue"]:
                print(el)
                print("")

            self.hero.lives -= 1
            print("++ You lost 1 life ++")

            if self.hero.lives == 0:
                return 0

        self.event = choose_enemy()

        self.fight(is_story=True)

        if self.fight_outcome == 1:
            print(story["story"][self.chapter]["won_dialogue"])

        else:
            print(story["story"][self.chapter]["lost_dialogue"])
            self.hero.lives = 0

        self.chapter += 1

    def chapter_3(self):
        self.print_chapter()
        with open("text_files/story.json", "r") as file:
            story = json.load(file)

        print(story["story"][self.chapter]["story"][0])
        print("")
        print(story["story"][self.chapter]["story"][1])
        print("")

        dial = story["story"][self.chapter]["dialogues"]

        for d in dial:
            print(d)
            print("")

        print(story["story"][self.chapter]["result"])
        self.hero.strength += 7
        self.hero.power += 7
        print("")

        print(story["story"][self.chapter]["ending"])
        print("")

        self.chapter += 1

    def chapter_4(self):
        self.print_chapter()
        with open("text_files/story.json", "r") as file:
            story = json.load(file)

        print(story["story"][self.chapter]["story"][0])
        print("")
        print(story["story"][self.chapter]["story"][1])
        print("")

        dial = story["story"][self.chapter]["dialogues"]

        for d in dial:
            print(d)
            print("")

        self.event = choose_enemy()

        self.fight(is_story=True)

        if self.fight_outcome == 1:
            print(story["story"][self.chapter]["ending"]["won_dialogue"])

            weapon = Weapon()
            if input("$ Do you agree?: (y/n) ").lower() in ["yes", "y"]:
                print("")
                print(f"+++ You gained a new weapon! - {weapon.show_weapon()} +++")
                print("")
                self.hero.weapons.append(weapon)

        else:
            print(story["story"][self.chapter]["ending"]["lost_dialogue"])
            self.hero.lives = 0

        self.chapter += 1

    def chapter_5(self):
        self.print_chapter()
        with open("text_files/story.json", "r") as file:
            story = json.load(file)

        print(story["story"][self.chapter]["story"][0])
        print("")

        dial = story["story"][self.chapter]["dialogues"]

        for d in dial:
            print(d)
            print("")

        print(story["story"][self.chapter]["reflection"])
        print("")

        self.chapter += 1

    def death(self):
        print("+++ You died +++")
        print("")
        print("1. Load the Game")
        print("2. Quit the Game")
        print("")

        c = 0

        while c < 1 or c > 2:
            c = int(input("$ What do you want to do?: "))

        if c == 1:
            self.load()

        elif c == 2:
            self.hero.lives = 0

    def print_chapter(self):
        print("###########################")
        print("#                         #")
        print(f"#        CHAPTER {self.chapter + 1}        #")
        print("#                         #")
        print("###########################")
