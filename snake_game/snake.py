from turtle import Turtle

UP = 90
DOWN = 270
RIGHT = 0
LEFT = 180

def first_segment():
    starting_positions = [(0, 0), (-20, 0), (-40, 0)]
    segments = []
    for i in range(3):
        new_turtle = Turtle(shape="square")
        new_turtle.color("white")
        new_turtle.penup()
        new_turtle.goto(starting_positions[i])
        segments.append(new_turtle)
    return segments


class Snake():
    def __init__(self):
        self.segments = first_segment()
        self.head = self.segments[0]
        self.direction = 0

    def up(self):
        if self. direction != DOWN:
            self.direction = UP

    def down(self):
        if self.direction != UP:
            self.direction = DOWN

    def right(self):
        if self.direction != LEFT:
            self.direction = RIGHT

    def left(self):
        if self.direction != RIGHT:
            self.direction = LEFT

    def move(self):
        for i in range(len(self.segments) - 1, 0, -1):
            x = self.segments[i - 1].xcor()
            y = self.segments[i - 1].ycor()
            self.segments[i].goto(x=x, y=y)
        self.segments[0].setheading(self.direction)
        self.segments[0].forward(20)

    def add_segment(self):
        new_turtle = Turtle(shape="square")
        new_turtle.color("white")
        new_turtle.penup()
        new_turtle.speed(0)
        self.segments.append(new_turtle)

    def collision(self):
        collision = False
        for i in range(1, len(self.segments) - 1):
            if self.segments[i].distance(self.head) <= 1:
                collision = True
                print('zderzenie')

        return collision






