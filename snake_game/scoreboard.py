from turtle import Turtle

file = open("high_score.txt", mode='r')
HIGH_SCORE = file.read()
file.close()

class ScoreBoard(Turtle):

    def __init__(self):
        super().__init__()
        self.goto(0, 280)
        self.speed(0)
        self.score = 0
        self.high_score = int(HIGH_SCORE)
        self.color('white')
        self.hideturtle()
        self.write(f"SCORE = {self.score}    HIGH SCORE = {self.high_score}", False, align="center",  font=("Arial", 13, "normal"))

    def refresh(self):
        self.score += 1
        self.clear()
        if self.score > self.high_score: 
            self.high_score = self.score
            file_2 = open("high_score.txt", mode='w')
            file_2.write(str(self.score))
            file_2.close()
        self.write(f"SCORE = {self.score}    HIGH SCORE = {self.high_score}", False, align="center", font=("Arial", 13, "normal"))

    def game_over(self):
        self.penup()
        self.goto(0, 0)
        self.write("GAME OVER", False, align="center", font=("Arial", 13, "normal"))



