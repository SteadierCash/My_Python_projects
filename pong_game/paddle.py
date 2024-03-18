from turtle import Turtle
import time


class Paddle(Turtle):
    def __init__(self, left_right):
        super().__init__()
        self.shape('square')
        self.penup()
        self.color('white')
        self.left_right = left_right
        self.goto(480 * self.left_right, 0)
        self.setheading(90)
        self.turtlesize(1, 5)

    def move_down(self):
        if self.ycor() > -230:
            self.forward(-40)

    def move_up(self):
        if self.ycor() < 240:
            self.forward(40)
