import os
import turtle
import time
import random

delay = 0.1
score = 0
high_score = 0

#screen 
wn = turtle.Screen()
wn.title("Wale's snake game")
wn.bgcolor('yellow')
wn.setup(width = 700 , height= 700)
wn.tracer(0)

#head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0,0)
head.direction = 'stop'

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("green")
food.penup()
food.goto(0,100)

segments = []

#pen
pen = turtle.Turtle()
pen.speed(0)
pen.color("black")
pen.penup()
pen.hideturtle()
pen.goto(0, 260)
pen.write("score: 0   High Score: 0", align = "center", font=("Courier", 24, "normal"))

#functions
def go_up() :
    if head.direction != 'down':
        head.direction = 'up'

def go_down() :
    if head.direction != 'up':
       head.direction = 'down'

def go_right() :
    if head.direction != "left" :
        head.direction = 'right'

def go_left():
    if head.direction != "right" :
        head.direction = 'left'


def move() :
    if head.direction == "up" :
        y = head.ycor()
        head.sety(y + 20)

    if head.direction == "right" :
        x = head.xcor()
        head.setx(x + 20)

    if head.direction == "left" :
        x = head.xcor()
        head.setx(x - 20)

    if head.direction == "down" :
        y = head.ycor()
        head.sety(y - 20)

#keyboard-bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "Down")
wn.onkeypress(go_left, "Left")
wn.onkeypress(go_right, "Right")





while True:
    wn.update()

    #collisoin
    if head.xcor() > 290 or head.xcor() < -290 or head.ycor() > 290 or head.ycor() < -290 :
        time.sleep(1)
        head.goto(0,0)
        head.direction = "stop"

    #hide the segments
        for segment in segments :
            segment.goto(1000,1000)

        segments.clear()

        delay = 0.1

        score = 0
        pen.clear()
        pen.write(f"score: {score}  High Score: {high_score}", align = "center", font=("Courier", 24, "normal"))


    if head.distance(food) < 20 :
        x = random.randint(-290, 290)
        y = random.randint(-290, 290)
        food.goto(x,y)

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("magenta")
        new_segment.penup()
        segments.append(new_segment)

        delay -= 0.01

        score += 10

        if score > high_score :
            high_score = score


        pen.clear()
        pen.write(f"score: {score}  High Score: {high_score}", align = "center", font=("Courier", 24, "normal"))

    for index in range(len(segments)-1 , 0 , -1) :
        x = segments[index-1].xcor()
        y = segments[index-1].ycor()    
        segments[index].goto(x,y)

    if len(segments) > 0 :
        x = head.xcor()
        y = head.ycor()
        segments[0].goto(x,y)

    move()

    for segment in segments :
        if segment.distance(head) < 20 :
            time.sleep(1)
            head.goto(0,0)
            head.direction = "stop"

            for seg in segments :
                seg.goto(1000,1000)

            segments.clear()

            delay = 0.1

            score = 0
            pen.clear()
            pen.write(f"score: {score}  High Score: {high_score}", align = "center", font=("Courier", 24, "normal"))
            break


    time.sleep(delay)


wn.mainloop()

