import os
import turtle
import time
import random

delay = 0.1

#screen 
wn = turtle.Screen()
wn.title("Wale's snake game")
wn.bgcolor('yellow')
wn.setup(width = 700 , height= 700)
# wn.tracer(0)


head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("blue")
head.penup()
head.goto(0,0)
head.direction = 'up'

food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("green")
food.penup()
head.goto(0,0)



def move() :
    if head.direction == 'up' :
        y = head.ycor()
        head.set(y + 20)


def go_up() :
    head.direction = "up"

def go_down() :
    head.direction = "down"

def go_left() :
    head.direction = "left"

def go_right() :
    head.direction = "right"


while True :
    wn.update()

    move()

    
wn.mainloop()

    # if head.distance(food) :
    #     x= head.xcor() 
    #     y= head.ycor()

    

    # time.sleep(delay)

