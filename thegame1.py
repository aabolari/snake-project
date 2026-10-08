# =======================================================================
# BEGINNER-FRIENDLY PYTHON TURTLE SNAKE GAME
# Standard Libraries: turtle, time, random (No pip packages needed)
# Easy to defend and explain line-by-line in presentations.
# =======================================================================

import turtle
import time
import random

# -----------------------------------------------------------------------
# SECTION 1: GAME CONFIGURATION & VARIABLES
# -----------------------------------------------------------------------
delay = 0.1       # Speed delay between game steps (0.1 seconds)
score = 0         # Player starting score
high_score = 0    # Session high score

# -----------------------------------------------------------------------
# SECTION 2: SCREEN SETUP & BOUNDARY GRID BOX
# -----------------------------------------------------------------------
win = turtle.Screen()
win.title("Beginner Snake Game - Python Turtle")
win.bgcolor("#1e293b")  # Dark background color
win.setup(width=650, height=650)
win.tracer(0)           # Turns off automatic screen animation for smooth frames

# Function that draws the visible boundary box where the snake runs
def draw_grid_box():
    pen = turtle.Turtle()
    pen.speed(0)
    pen.color("#38bdf8")  # Sky-blue border color
    pen.pensize(4)
    pen.penup()
    # Move to the top-left corner of the playable area
    pen.goto(-290, 290)
    pen.pendown()
    # Draw a 580x580 square border using a simple for loop
    for _ in range(4):
        pen.forward(580)
        pen.right(90)
    pen.hideturtle()

# Call the function to draw the grid boundary box
draw_grid_box()

# -----------------------------------------------------------------------
# SECTION 3: CREATING GAME OBJECTS (HEAD, FOOD, SCOREBOARD)
# -----------------------------------------------------------------------
# 1. Snake Head
head = turtle.Turtle()
head.speed(0)
head.shape("square")
head.color("#22c55e")  # Green snake head
head.penup()
head.goto(0, 0)        # Center of the grid
head.direction = "stop"

# 2. Food
food = turtle.Turtle()
food.speed(0)
food.shape("circle")
food.color("#ef4444")  # Red apple
food.penup()
food.goto(0, 100)

# 3. List to hold trailing body segments
segments = []

# 4. Scoreboard Pen
score_pen = turtle.Turtle()
score_pen.speed(0)
score_pen.color("#f8fafc")
score_pen.penup()
score_pen.hideturtle()
score_pen.goto(0, 260)
score_pen.write("Score: 0   High Score: 0", align="center", font=("Arial", 16, "bold"))

# -----------------------------------------------------------------------
# SECTION 4: DEFINED FUNCTIONS FOR CONTROLS & MOVEMENT
# -----------------------------------------------------------------------
# Steering functions: IF statements prevent 180-degree self-reversals
def go_up():
    if head.direction != "down":
        head.direction = "up"

def go_down():
    if head.direction != "up":
        head.direction = "down"

def go_left():
    if head.direction != "right":
        head.direction = "left"

def go_right():
    if head.direction != "left":
        head.direction = "right"

# Move function: IF and ELIF statements update head position by 20 pixels
def move():
    if head.direction == "up":
        y = head.ycor()
        head.sety(y + 20)
    elif head.direction == "down":
        y = head.ycor()
        head.sety(y - 20)
    elif head.direction == "left":
        x = head.xcor()
        head.setx(x - 20)
    elif head.direction == "right":
        x = head.xcor()
        head.setx(x + 20)

# -----------------------------------------------------------------------
# SECTION 5: KEYBOARD LISTENERS
# -----------------------------------------------------------------------
win.listen()
# Arrow keys
win.onkey(go_up, "Up")
win.onkey(go_down, "Down")
win.onkey(go_left, "Left")
win.onkey(go_right, "Right")
# WASD keys
win.onkey(go_up, "w")
win.onkey(go_down, "s")
win.onkey(go_left, "a")
win.onkey(go_right, "d")

# -----------------------------------------------------------------------
# SECTION 6: MAIN GAME LOOP (WHILE LOOP)
# -----------------------------------------------------------------------
while True:
    win.update()  # Manually refresh the screen each tick

    # 1. CHECK WALL COLLISION: Grid box boundaries are -280 to +280
    if head.xcor() > 280 or head.xcor() < -280 or head.ycor() > 280 or head.ycor() < -280:
        time.sleep(0.5)      # Brief pause upon crash
        head.goto(0, 0)
        head.direction = "stop"

        # Hide body segments off screen
        for segment in segments:
            segment.goto(1000, 1000)
        segments.clear()     # Empty the list

        score = 0
        score_pen.clear()
        score_pen.write(f"Score: {score}   High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

    # 2. CHECK FOOD COLLISION: Distance < 20 pixels
    if head.distance(food) < 20:
        # Spawn food in random grid tile (multiples of 20)
        x = random.randint(-13, 13) * 20
        y = random.randint(-13, 13) * 20
        food.goto(x, y)

        # Append new body segment
        new_segment = turtle.Turtle()
        new_segment.speed(0)
        new_segment.shape("square")
        new_segment.color("#86efac")  # Light green body
        new_segment.penup()
        segments.append(new_segment)

        score += 10
        if score > high_score:
            high_score = score
        score_pen.clear()
        score_pen.write(f"Score: {score}   High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

    # 3. MOVE BODY SEGMENTS: Reverse FOR loop (tail moves to prior segment)
    for index in range(len(segments) - 1, 0, -1):
        prev_x = segments[index - 1].xcor()
        prev_y = segments[index - 1].ycor()
        segments[index].goto(prev_x, prev_y)

    # First segment moves to where the head was
    if len(segments) > 0:
        segments[0].goto(head.xcor(), head.ycor())

    # 4. MOVE HEAD
    move()

    # 5. CHECK SELF COLLISION: Head hits any segment in the list
    for segment in segments:
        if segment.distance(head) < 20:
            time.sleep(0.5)
            head.goto(0, 0)
            head.direction = "stop"

            for seg in segments:
                seg.goto(1000, 1000)
            segments.clear()

            score = 0
            score_pen.clear()
            score_pen.write(f"Score: {score}   High Score: {high_score}", align="center", font=("Arial", 16, "bold"))

    time.sleep(delay)  # Controls game speed