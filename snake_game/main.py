from turtle import Screen
from snake import Snake
from food import Food
import time
from scoreboard import ScoreBoard

screen = Screen()
screen.setup(width=600, height=600)
screen.bgcolor("black")
screen.title("My snake game")
screen.tracer(0)

snake = Snake()
food = Food()

screen.listen()
screen.onkey(key="Up", fun=snake.up)
screen.onkey(key="Down", fun=snake.down)
screen.onkey(key="Right", fun=snake.right)
screen.onkey(key="Left", fun=snake.left)

game_is_on = True

scoreboard = ScoreBoard()

while game_is_on:
    snake.move()
    screen.update()
    time.sleep(0.1)

    if snake.head.distance(food) < 1:
        snake.add_segment()
        scoreboard.refresh()
        food.refresh()

    is_col = snake.collision()

    if (snake.head.xcor() < -280 or snake.head.xcor() > 280 or snake.head.ycor() < -280 or snake.head.ycor() > 280
            or is_col):
        scoreboard.game_over()
        game_is_on = False

screen.exitonclick()
