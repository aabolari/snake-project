# game_engine.py - the rules of the game. NO turtle code in this file.
#
# The whole game lives in one dictionary called `state`:
#
#   state = {
#       "snakes":    [snake, ...],   # list of snake dictionaries (one for now)
#       "food":      (x, y) or None, # a cell
#       "obstacles": [(x, y), ...],  # cells (must be tuples)
#       "high_score": 0,
#       "status":    "running" | "paused" | "game_over",
#   }
#
# and each snake is a dictionary:
#
#   snake = {
#       "name": "player",
#       "controller": "human",       # later: "ai"
#       "body": [(x, y), ...],       # body[0] is the HEAD, body[-1] is the tail
#       "direction": "right",        # the direction used for the last move
#       "next_direction": "up",      # the direction requested for the next move
#       "score": 0,
#       "alive": True,
#   }

import random
from config import (
    GRID_MIN, GRID_MAX,
    DIRECTION_VECTORS, OPPOSITE_DIRECTION,
    POINTS_PER_FOOD,
)


# ----------------------------------------------------------------------
# Creating things
# ----------------------------------------------------------------------
def create_snake(name, start_cell=(0, 0), controller="human"):
    """Return a new snake dictionary: length 1, waiting for its first move."""
    return {
        "name": name,
        "controller": controller,
        "body": [start_cell],
        "direction": "stop",
        "next_direction": "stop",
        "score": 0,
        "alive": True,
    }


def new_game_state(high_score=0):
    """Return a fresh game state. The high score can carry over between rounds."""
    state = {
        "snakes": [create_snake("player")],
        "food": None,
        "obstacles": [],
        "high_score": high_score,
        "status": "running",
    }
    state["food"] = spawn_food(state)
    return state


def spawn_food(state):
    """Return a random EMPTY cell (not on any snake or obstacle), or None if the board is full."""
    taken = set(state["obstacles"])
    for snake in state["snakes"]:
        taken.update(snake["body"])

    free_cells = []
    for x in range(GRID_MIN, GRID_MAX + 1):
        for y in range(GRID_MIN, GRID_MAX + 1):
            if (x, y) not in taken:
                free_cells.append((x, y))

    if not free_cells:
        return None
    return random.choice(free_cells)


# ----------------------------------------------------------------------
# Steering
# ----------------------------------------------------------------------
def change_direction(snake, new_direction):
    """Request a new direction. A 180-degree reverse is ignored.

    The request is stored in next_direction and only applied on the next
    game step, so pressing two keys quickly can never reverse the snake
    into itself.
    """
    if new_direction == OPPOSITE_DIRECTION.get(snake["direction"]):
        return
    snake["next_direction"] = new_direction


# ----------------------------------------------------------------------
# Collision checks: each one returns True (collision) or False
# ----------------------------------------------------------------------
def check_wall_collision(cell):
    x, y = cell
    return x < GRID_MIN or x > GRID_MAX or y < GRID_MIN or y > GRID_MAX


def check_self_collision(snake, cell, growing):
    """Would `cell` hit this snake's own body?

    If the snake is not growing, its tail leaves its cell this step, so
    the tail cell is safe to move into.
    """
    body_to_check = snake["body"] if growing else snake["body"][:-1]
    return cell in body_to_check


def check_obstacle_collision(state, cell):
    return cell in state["obstacles"]


# ----------------------------------------------------------------------
# Moving
# ----------------------------------------------------------------------
def get_next_head(snake):
    """The cell the head will enter on this step."""
    dx, dy = DIRECTION_VECTORS[snake["direction"]]
    head_x, head_y = snake["body"][0]
    return (head_x + dx, head_y + dy)


def move_snake(snake, new_head, growing):
    """Move the whole snake one cell.

    Add the new head at the front. Remove the tail unless the snake is
    growing. This one step is the body-following logic: every segment
    ends up where the one in front of it used to be.
    """
    snake["body"].insert(0, new_head)
    if not growing:
        snake["body"].pop()


# ----------------------------------------------------------------------
# One game step
# ----------------------------------------------------------------------
def update_game(state):
    """Advance the game by one step. Order: steer, check, move, eat."""
    for snake in state["snakes"]:
        if not snake["alive"]:
            continue

        snake["direction"] = snake["next_direction"]
        if snake["direction"] == "stop":
            continue                      # waiting for the first key press

        new_head = get_next_head(snake)
        growing = (new_head == state["food"])

        if (check_wall_collision(new_head)
                or check_self_collision(snake, new_head, growing)
                or check_obstacle_collision(state, new_head)):
            snake["alive"] = False
            continue

        move_snake(snake, new_head, growing)

        if growing:
            snake["score"] += POINTS_PER_FOOD
            state["high_score"] = max(state["high_score"], snake["score"])
            state["food"] = spawn_food(state)

    # TEAM DECISION NEEDED (Member 1): snake-vs-snake collisions go here,
    # before the game-over check below.

    # TEAM DECISION NEEDED: right now the game ends when ANY snake dies.
    for snake in state["snakes"]:
        if not snake["alive"]:
            state["status"] = "game_over"


# ----------------------------------------------------------------------
# Pause and restart
# ----------------------------------------------------------------------
def toggle_pause(state):
    if state["status"] == "running":
        state["status"] = "paused"
    elif state["status"] == "paused":
        state["status"] = "running"


def reset_game(state):
    """Start a new round inside the SAME state dictionary. High score is kept."""
    fresh = new_game_state(state["high_score"])
    state.clear()
    state.update(fresh)
