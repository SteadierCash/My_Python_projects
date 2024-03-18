from turtle import Turtle
import time


class Score(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.penup()
        self.color('white')
        self.left_score = 0
        self.right_score = 0
        self.turtlesize(0.5, 0.5)
        self.hideturtle()

    def draw_score(self, left_right):
        self.goto(50 * left_right, 230)
        self.setheading(90)
        for i in range(5):
            self.stamp()
            self.forward(10)

