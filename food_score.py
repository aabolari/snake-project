import turtle
import random

# Window
wn = turtle.Screen()
wn.title("Snake - Food and Score")
wn.bgcolor("black")
wn.setup(width=600, height=600)
wn.tracer(0)

# Head (temporary: moves by key press just for testing)
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("green")
head.penup()
head.goto(0, 0)

# 1. Creating the food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("red")
food.penup()
food.goto(0, 100)

# Score display
score = 0
pen = turtle.Turtle()
pen.speed(0)
pen.color("white")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)

def update_score():
    pen.clear()
    pen.write(f"Score: {score}", align="center", font=("Courier", 24, "normal"))

update_score()

# Temporary movement functions
def go_up():    head.sety(head.ycor() + 20)
def go_down():  head.sety(head.ycor() - 20)
def go_left():  head.setx(head.xcor() - 20)
def go_right(): head.setx(head.xcor() + 20)

wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")

# Game loop
while True:
    wn.update()

    # 2. Detecting when the snake reaches the food
    if head.distance(food) < 20:
        # 3 & 4. Random position, moving the food after it's eaten
        x = random.randint(-14, 14) * 20
        y = random.randint(-14, 14) * 20
        food.goto(x, y)

        # 5 & 6. Increase the score and display it
        score += 10
        update_score()