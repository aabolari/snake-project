# ui.py - everything you SEE or PRESS. This file only draws the state and
# forwards key presses. It never moves snakes or checks collisions.

import turtle
from config import (
    CELL_SIZE, GRID_MAX, WINDOW_SIZE,
    BACKGROUND_COLOUR, BORDER_COLOUR, HEAD_COLOUR, BODY_COLOUR,
    FOOD_COLOUR, OBSTACLE_COLOUR, TEXT_COLOUR, KEY_DIRECTIONS,
)

# The few turtles we create ONCE and reuse every frame.
pens = {}


def setup_screen():
    win = turtle.Screen()
    win.title("Snake Game - Python Turtle")
    win.bgcolor(BACKGROUND_COLOUR)
    win.setup(width=WINDOW_SIZE, height=WINDOW_SIZE)
    win.tracer(0)             # we refresh the screen ourselves, once per frame
    return win

def draw_grid():
    """Draw a faint grid inside the playable area."""
    half = (GRID_MAX + 0.5) * CELL_SIZE      # Matches the border boundaries exactly
    grid_pen = turtle.Turtle()
    grid_pen.hideturtle()
    grid_pen.speed(0)
    
    # Matches the dark theme BACKGROUND_COLOUR ("#1e293b") from config.py[cite: 4]
    grid_pen.color("#334155") 
    grid_pen.pensize(1)
    grid_pen.penup()

    start = int(-half)
    end = int(half)

    # Draw vertical lines
    for x in range(start, end + 1, CELL_SIZE):
        grid_pen.goto(x, end)
        grid_pen.pendown()
        grid_pen.goto(x, start)
        grid_pen.penup()

    # Draw horizontal lines
    for y in range(start, end + 1, CELL_SIZE):
        grid_pen.goto(start, y)
        grid_pen.pendown()
        grid_pen.goto(end, y)
        grid_pen.penup()

def draw_board():
    """Draw the border around the playable area (drawn once)."""
    half = (GRID_MAX + 0.5) * CELL_SIZE      # 290 pixels with the default config
    border = turtle.Turtle()
    border.hideturtle()
    border.speed(0)
    border.color(BORDER_COLOUR)
    border.pensize(4)
    border.penup()
    border.goto(-half, half)
    border.pendown()
    for corner in [(half, half), (half, -half), (-half, -half), (-half, half)]:
        border.goto(corner)


def create_pens():
    """Create the three reusable turtles: painter, scoreboard and message."""
    painter = turtle.Turtle()           # stamps snakes, food and obstacles
    painter.hideturtle()
    painter.speed(0)
    painter.penup()

    scoreboard = turtle.Turtle()
    scoreboard.hideturtle()
    scoreboard.speed(0)
    scoreboard.penup()
    scoreboard.color(TEXT_COLOUR)
    scoreboard.goto(0, 300)

    message = turtle.Turtle()
    message.hideturtle()
    message.speed(0)
    message.penup()
    message.color(TEXT_COLOUR)
    message.goto(0, -10)

    modal = turtle.Turtle()
    modal.hideturtle()
    modal.speed(0)
    modal.penup()

    pens["painter"] = painter
    pens["scoreboard"] = scoreboard
    pens["message"] = message
    pens["modal"] = modal

def setup_ui():
    """Call once at startup. Returns the screen."""
    win = setup_screen()
    draw_board()
    draw_grid()
    create_pens()
    return win


# ----------------------------------------------------------------------
# Drawing the state
# ----------------------------------------------------------------------
def stamp_cell(cell, shape, colour):
    """Draw one cell. This is the ONLY place cells become pixels."""
    painter = pens["painter"]
    x, y = cell
    painter.shape(shape)
    painter.color(BACKGROUND_COLOUR, colour)   # outline, fill
    painter.goto(x * CELL_SIZE, y * CELL_SIZE)
    painter.stamp()


def draw_game(state):
    """Redraw everything from the state, then refresh the screen once."""
    pens["painter"].clearstamps()

    if state["food"] is not None:
        stamp_cell(state["food"], "circle", FOOD_COLOUR)

    for cell in state["obstacles"]:
        stamp_cell(cell, "square", OBSTACLE_COLOUR)

    for snake in state["snakes"]:
        for index, cell in enumerate(snake["body"]):
            colour = HEAD_COLOUR if index == 0 else BODY_COLOUR
            stamp_cell(cell, "square", colour)


    update_scoreboard(state)

    if state["status"] == "menu":
        pens["scoreboard"].clear() # Hide scoreboard on menu
        draw_main_menu(state)
    elif state["status"] == "game_over":
        pens["message"].clear() # Hide normal pause messages
        draw_game_over(state)
    else:
        pens["modal"].clear() # Ensure the modal disappears when playing
        show_status_message(state)
        
    turtle.update()



def update_scoreboard(state):
    scoreboard = pens["scoreboard"]
    scoreboard.clear()
    score = state["snakes"][0]["score"]       # Member 3: show every snake here later
    scoreboard.write(
        f"Score: {score}   High Score: {state['high_score']}",
        align="center", font=("Arial", 16, "bold"),
    )


def show_status_message(state):
    message = pens["message"]
    message.clear()
    if state["status"] == "paused":
        message.write("PAUSED - press SPACE to resume",
                      align="center", font=("Arial", 18, "bold"))
    elif state["status"] == "game_over":
        message.write("GAME OVER - press R to restart",
                      align="center", font=("Arial", 18, "bold"))


# In ui.py
def draw_ui_card(pen, cx, cy, width, height, theme_color, fill_color, title, subtitle):
    """Draws a stylized, clickable card centered at (cx, cy) with a solid background."""
    start_x = cx - (width / 2)
    start_y = cy + (height / 2)

    # 1. Draw the card outline and filled background
    pen.penup()
    pen.goto(start_x, start_y)
    # The first argument is the border, the second is the inner fill
    pen.color(theme_color, fill_color) 
    pen.pensize(3)
    pen.pendown()
    
    pen.begin_fill() # Start tracking the shape area
    for _ in range(2):
        pen.forward(width)
        pen.right(90)
        pen.forward(height)
        pen.right(90)
    pen.end_fill() # Physically paint the interior
    pen.penup()

    # 2. Draw the Title (Must happen AFTER end_fill)
    pen.goto(cx, cy + 5)
    pen.color(TEXT_COLOUR)
    pen.write(title, align="center", font=("Arial", 16, "bold"))

    # 3. Draw the Subtitle
    pen.goto(cx, cy - 20)
    pen.color(theme_color)
    pen.write(subtitle, align="center", font=("Arial", 10, "normal"))


# In ui.py
def draw_main_menu(state):
    modal = pens["modal"]
    modal.clear()
    
    if state["status"] != "menu":
        return

    # Draw Header
    modal.goto(0, 180)
    modal.color(TEXT_COLOUR)
    modal.write("SNAKE ARENA", align="center", font=("Arial", 28, "bold"))
    modal.goto(0, 140)
    modal.write("CHOOSE YOUR GAME MODE", align="center", font=("Arial", 12, "normal"))

    # Card 1: Sky Blue Border, Deep Slate Background
    draw_ui_card(modal, 0, 60, 300, 80, BORDER_COLOUR, "#0f172a", "SINGLE PLAYER", "Classic snake experience")
    
    # Card 2: Bright Green Border, Dark Emerald Background
    draw_ui_card(modal, 0, -40, 300, 80, HEAD_COLOUR, "#064e3b", "MULTIPLAYER", "Challenge another player")
    
    # Card 3: Bright Red Border, Dark Crimson Background
    draw_ui_card(modal, 0, -140, 300, 80, FOOD_COLOUR, "#450a0a", "VS AI", "Play against the smart snake")


def draw_game_over(state):
    modal = pens["modal"]
    modal.clear() # CRITICAL: Prevents ghosting from previous frames

    # Only draw if the game is actually over
    if state["status"] != "game_over":
        return

    # 1. Draw the background box
    modal.goto(-150, 100)
    modal.color(BORDER_COLOUR, "#0f172a") # Border color, darker fill
    modal.pendown()
    modal.pensize(2)
    modal.begin_fill()
    for _ in range(2):
        modal.forward(300)
        modal.right(90)
        modal.forward(200)
        modal.right(90)
    modal.end_fill()
    modal.penup()

    # 2. Draw the text
    modal.goto(0, 40)
    modal.color("#f87171") # Soft Red
    modal.write("GAME OVER", align="center", font=("Arial", 24, "bold"))

    modal.goto(0, 0)
    modal.color(TEXT_COLOUR)
    score = state["snakes"][0]["score"]
    high_score = state["high_score"]
    modal.write(f"SCORE: {score}   HIGH: {high_score}", align="center", font=("Arial", 14, "normal"))

    modal.goto(0, -50)
    modal.color(HEAD_COLOUR) # Use the snake green for the button text
    modal.write("Press SPACE to Restart", align="center", font=("Arial", 14, "bold"))


# ----------------------------------------------------------------------
# Keyboard
# ----------------------------------------------------------------------
def bind_keys(on_direction, on_pause, on_restart, on_menu_click):
    """Connect keys to functions that main.py provides."""
    win = turtle.Screen()
    win.listen()
    for key, direction in KEY_DIRECTIONS.items():
        win.onkeypress(lambda d=direction: on_direction(d), key)
    win.onkeypress(on_pause, "space")
    win.onkeypress(on_pause, "p")
    win.onkeypress(on_restart, "r")

    # The Hit-Testing Function
    def handle_mouse_click(x, y):
        # Check X bounds (Width is 300, so -150 to 150)
        if -150 <= x <= 150:
            # Card 1: Y=60, Height=80 (Bounds: 20 to 100)
            if 20 <= y <= 100:
                on_menu_click("single")
            # Card 2: Y=-40, Height=80 (Bounds: -80 to 0)
            elif -80 <= y <= 0:
                on_menu_click("multi")
            # Card 3: Y=-140, Height=80 (Bounds: -180 to -100)
            elif -180 <= y <= -100:
                on_menu_click("ai")

    # Bind the left mouse button (btn=1) to our hit-testing function
    win.onscreenclick(handle_mouse_click, btn=1)
