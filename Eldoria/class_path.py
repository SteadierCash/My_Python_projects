from paths import paths
import random
import json


def read_actions(chapter):
    actions = (["shop"] * 3 + ["fight"] * 10 + ["friend"] * 4)

    if chapter < 6:
        actions += ["story"] * 6

    action = random.choice(actions)

    with open("text_files/" + action + ".json", "r") as file:
        events = json.load(file)

    if action == "story":
        return events["story"][chapter]
    else:
        return random.choice(events)


class Path:
    def __init__(self, chapter):
        self.left_path = read_actions(chapter)
        self.straight_path = read_actions(chapter)
        self.right_path = read_actions(chapter)

        # drowning paths
        self.path = paths(self.left_path["action"], self.straight_path["action"], self.right_path["action"])

    def draw_path(self):
        print(self.path)

    def ask_for_action(self):
        p = [self.left_path, self.straight_path, self.right_path]

        action = -1

        while 0 > action or action > 2:
            print("0: up, 1: right, 2: down")
            action = int(input("$ Where do you want to go?: "))
            print("")

        return p[action]
