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

    pens["painter"] = painter
    pens["scoreboard"] = scoreboard
    pens["message"] = message


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


# ----------------------------------------------------------------------
# Keyboard
# ----------------------------------------------------------------------
def bind_keys(on_direction, on_pause, on_restart):
    """Connect keys to functions that main.py provides."""
    win = turtle.Screen()
    win.listen()
    for key, direction in KEY_DIRECTIONS.items():
        win.onkeypress(lambda d=direction: on_direction(d), key)
    win.onkeypress(on_pause, "space")
    win.onkeypress(on_pause, "p")
    win.onkeypress(on_restart, "r")
