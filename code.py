import os
import turtle
import time
import random

delay = 0.15
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
pen.goto(0, 300)
pen.write("score: 0   High Score: 0", align = "center", font=("Courier", 24, "normal"))

# Draw the border
border_pen = turtle.Turtle()
border_pen.speed(0)
border_pen.color("orange")  # Feel free to change the border color
border_pen.pensize(1)      # Adjust thickness 
border_pen.penup()
border_pen.goto(-310, -310) # Start at the bottom-left corner
border_pen.pendown()

# Draw a 600x600 square
for _ in range(4):
    border_pen.forward(600)
    border_pen.left(90)

border_pen.hideturtle()

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

def auto_steer():
    hx, hy = head.xcor(), head.ycor()
    fx, fy = food.xcor(), food.ycor()

    # 1. Map out where each possible move would land
    moves = {
        "up": (hx, hy + 20),
        "down": (hx, hy - 20),
        "left": (hx - 20, hy),
        "right": (hx + 20, hy)
    }

    # 2. Identify the illegal reverse direction
    opposites = {"up": "down", "down": "up", "left": "right", "right": "left", "stop": None}
    reverse_dir = opposites.get(head.direction)

    # 3. Filter out moves that result in immediate death
    safe_moves = []
    for direction, (nx, ny) in moves.items():
        # Prevent 180-degree reverse turn if we have a body
        if len(segments) > 0 and direction == reverse_dir:
            continue
            
        # Avoid walls
        if nx > 290 or nx < -290 or ny > 290 or ny < -290:
            continue
            
        # Avoid the snake's own body
        hit_body = False
        for segment in segments:
            if segment.distance((nx, ny)) < 15: 
                hit_body = True
                break
                
        if not hit_body:
            safe_moves.append(direction)

    # 4. If trapped, do nothing (game over)
    if not safe_moves:
        return

    # 5. Of the safe moves, pick the one closest to the food
    best_move = safe_moves[0]
    min_distance = float('inf')

    for direction in safe_moves:
        nx, ny = moves[direction]
        distance = abs(nx - fx) + abs(ny - fy)
        
        if distance < min_distance:
            min_distance = distance
            best_move = direction

    # 6. Command the snake
    head.direction = best_move


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


def place_food():
    while True:
        food.goto(random.randrange(-280, 281, 20), random.randrange(-280, 281, 20))
        blocked = food.distance(head) < 20
        for s in segments:
            if food.distance(s) < 20:
                blocked = True
        if not blocked:
            break


#keyboard-bindings
wn.listen()
wn.onkeypress(go_up, "Up")
wn.onkeypress(go_down, "s")
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
        place_food()

        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("magenta")
        new_segment.penup()
        segments.append(new_segment)

        delay = max(0.03, delay - 0.01)

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

    # Inject the AI here!
    # auto_steer() 

    move() # The snake now executes the AI's chosen move

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