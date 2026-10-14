# config.py - shared constants. Change numbers here, not inside other files.
#
# COORDINATE SYSTEM (agreed by everyone):
#   Every position in the game is a CELL: a tuple (x, y) of whole numbers.
#   (0, 0) is the centre of the board. x grows to the right, y grows upwards.
#   Only ui.py ever converts cells to pixels (cell * CELL_SIZE).

CELL_SIZE = 20          # pixels per cell (used only by ui.py)
GRID_MIN = -14          # smallest x or y cell
GRID_MAX = 14           # largest x or y cell  -> a 29 x 29 board
                        # (keep GRID_MIN == -GRID_MAX so the board stays centred)

TICK_MS = 100           # milliseconds between game steps (lower = faster)
POINTS_PER_FOOD = 10

# DIRECTIONS are plain strings: "up", "down", "left", "right"
# "stop" is the starting direction: the snake waits until the first key press.
DIRECTION_VECTORS = {
    "up": (0, 1),
    "down": (0, -1),
    "left": (-1, 0),
    "right": (1, 0),
}

OPPOSITE_DIRECTION = {
    "up": "down",
    "down": "up",
    "left": "right",
    "right": "left",
}

# Keyboard: key name -> direction
KEY_DIRECTIONS = {
    "Up": "up", "Down": "down", "Left": "left", "Right": "right",
    "w": "up", "s": "down", "a": "left", "d": "right",
    "W": "up", "S": "down", "A": "left", "D": "right",
}

# Look and feel (Member 3 can change these freely)
WINDOW_SIZE = 700
BACKGROUND_COLOUR = "#1e293b"
BORDER_COLOUR = "#38bdf8"
HEAD_COLOUR = "#22c55e"
BODY_COLOUR = "#86efac"
FOOD_COLOUR = "#ef4444"
OBSTACLE_COLOUR = "#94a3b8"
TEXT_COLOUR = "#f8fafc"


# ----------------------------------------------------------------------
# Versus modes: 1v1 human ("multi") and human vs AI ("ai")
# ----------------------------------------------------------------------
# Two key groups. In 1v1, P1 uses WASD and P2 uses the arrow keys.
# In single player and vs AI, both groups steer the same human snake.
ARROW_KEYS = {"Up": "up", "Down": "down", "Left": "left", "Right": "right"}
WASD_KEYS = {
    "w": "up", "s": "down", "a": "left", "d": "right",
    "W": "up", "S": "down", "A": "left", "D": "right",
}

P1_START = (-8, 0)      # where snake 1 starts
P2_START = (8, 0)       # where snake 2 (or the AI) starts

# (head colour, body colour) for snake 1 and snake 2
SNAKE_COLOURS = [(HEAD_COLOUR, BODY_COLOUR), ("#f59e0b", "#fcd34d")]

# Chance (0 to 1) that the AI ignores the food and makes a random safe move
AI_MISTAKE_CHANCE = {"easy": 0.35, "medium": 0.12, "hard": 0.0}
