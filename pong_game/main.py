import time
from turtle import Screen, Turtle
from paddle import Paddle
from ball import Ball
from score import Score

screen = Screen()
screen.setup(width=1040, height=630)
screen.bgcolor('black')

screen.tracer(0)

dot_line = Turtle('square')
dot_line.turtlesize(0.25, 0.5)
dot_line.color('white')
dot_line.penup()
dot_line.goto(0, -300)
dot_line.setheading(90)
dot_line.speed(0)
dot_line.ht()


def draw_line(heading):
    dot_line.setheading(heading)
    dot_line.stamp()
    dot_line.forward(25)
    dot_line.stamp()
    dot_line.forward(25)
    dot_line.stamp()


directions = [[300, 90, dot_line.ycor], [500, 0, dot_line.xcor], [-300, 270, dot_line.ycor],
              [-500, 180, dot_line.xcor], [300, 90, dot_line.ycor],  [500, 0, dot_line.xcor]]

for direct in directions:
    while direct[2]() != direct[0]:
        draw_line(direct[1])


left_paddle = Paddle(-1)
right_paddle = Paddle(1)
ball = Ball()

screen.update()
time.sleep(1)

screen.tracer(1)
screen.listen()

screen.onkey(key='Up', fun=right_paddle.move_up)
screen.onkey(key='Down', fun=right_paddle.move_down)

screen.onkey(key='w', fun=left_paddle.move_up)
screen.onkey(key='s', fun=left_paddle.move_down)

game_on = True

score = Score()
score.draw_score(-1)
score.draw_score(1)

while game_on:
    if -480 >= ball.xcor() or ball.xcor() >= 480:
        time.sleep(1)
        ball.ht()
        screen.tracer(0)
        ball = Ball()
        screen.tracer(1)

    elif ball.distance(left_paddle) < 40 or ball.distance(right_paddle) < 40:
        screen.tracer(0)
        ball.bounce_from_x()
        screen.update()
        screen.tracer(1)

    elif 280 <= ball.ycor() or ball.ycor() <= -280:
        screen.tracer(0)
        ball.bounce_from_y()
        screen.update()
        screen.tracer(1)


    ball.move()

screen.exitonclick()
