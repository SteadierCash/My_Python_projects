from turtle import Turtle
import random


class Ball(Turtle):
    def __init__(self):
        super().__init__()
        self.shape('square')
        self.color('white')
        self.speed(2)
        self.penup()
        self.bounce_x_old = 0
        self.bounce_y_old = 0
        self.bounce_x_new = 0
        self.bounce_y_new = 0
        self.direct = (random.randint(0, 360))
        self.setheading(self.direct)
        self.settiltangle(-self.direct)

    def move(self):
        self.forward(10)

    def bounce_from_y(self):
        self.bounce_x_old = self.bounce_x_new
        self.bounce_y_old = self.bounce_y_new
        self.bounce_x_new = self.xcor()
        self.bounce_y_new = self.ycor()
        self.direct = self.towards((2 * self.bounce_x_new - self.bounce_x_old), self.bounce_y_old)
        self.setheading(self.direct)
        self.settiltangle(-self.direct)

    def bounce_from_x(self):
        self.bounce_x_old = self.bounce_x_new
        self.bounce_y_old = self.bounce_y_new
        self.bounce_x_new = self.xcor()
        self.bounce_y_new = self.ycor()
        self.direct = self.towards(self.bounce_x_old, (2 * self.bounce_y_new - self.bounce_y_old))
        self.setheading(self.direct)
        self.settiltangle(-self.direct)


