from turtle import Turtle
import random

class Food(Turtle):

    def __init__(self):
        super().__init__()
        self.shape("circle")
        self.color("blue")
        self.shapesize(stretch_wid=0.5, stretch_len=0.5)
        self.penup()
        self.speed(0)
        self.refresh()

    def refresh(self):
        random_x = 20 * random.randint(-14, 14)
        random_y = 20 * random.randint(-14, 14)
        self.goto(random_x, random_y)



