# ai_player.py - the computer player, in three layers (one new idea per level):
#
#   EASY   : plays safe (never walks into a wall, itself or an obstacle),
#            heads for the food, but 35% of the time picks a random safe move.
#   MEDIUM : the same, but only makes a random move 12% of the time.
#   HARD   : never makes random moves, and also checks that a move does not
#            trap the snake in a dead end (it counts the free space left).
#
# The AI follows exactly the same rules as a human: it only chooses a
# direction. The game engine does the moving.

import random
import game_engine
from config import DIRECTION_VECTORS, OPPOSITE_DIRECTION, AI_MISTAKE_CHANCE


def cell_after_move(snake, direction):
    """The cell the head would enter if the snake went in this direction."""
    dx, dy = DIRECTION_VECTORS[direction]
    head_x, head_y = snake["body"][0]
    return (head_x + dx, head_y + dy)


def get_safe_moves(state, snake):
    """Every direction that does not reverse and does not kill the snake.

    Returns a list of (direction, new_head) pairs. It uses the engine's own
    collision checks, so obstacles added by teammates are avoided automatically.
    """
    safe = []
    for direction in DIRECTION_VECTORS:
        if direction == OPPOSITE_DIRECTION.get(snake["direction"]):
            continue                            # a 180 degree turn is not allowed
        new_head = cell_after_move(snake, direction)
        growing = (new_head == state["food"])
        if (game_engine.check_wall_collision(new_head)
                or game_engine.check_self_collision(snake, new_head, growing)
                or game_engine.check_obstacle_collision(state, new_head)):
            continue
        safe.append((direction, new_head))
    return safe


def distance_to(cell, target):
    """How many steps apart two cells are if you can't move diagonally."""
    return abs(cell[0] - target[0]) + abs(cell[1] - target[1])


def count_open_cells(state, body, start):
    """Flood fill: count the free cells you can walk to from `start`.

    Cells blocked by a wall, an obstacle or the snake's own body are not
    counted. The tail is not a wall because it moves away.
    """
    blocked = set(state["obstacles"])
    blocked.update(body[:-1])
    seen = {start}
    queue = [start]
    while len(queue) > 0:
        x, y = queue.pop(0)
        for dx, dy in DIRECTION_VECTORS.values():
            neighbour = (x + dx, y + dy)
            if game_engine.check_wall_collision(neighbour):
                continue
            if neighbour in seen or neighbour in blocked:
                continue
            seen.add(neighbour)
            queue.append(neighbour)
    return len(seen)


def choose_ai_direction(state, snake, level):
    """Pick the direction for the AI snake's next step. level is "easy", "medium" or "hard"."""
    options = get_safe_moves(state, snake)

    if len(options) == 0:
        return snake["direction"]               # trapped: every move kills it

    # a random "mistake" (still a safe move). This is what separates the levels.
    if state["food"] is None or random.random() < AI_MISTAKE_CHANCE[level]:
        return random.choice(options)[0]

    best_direction = None
    best_score = None
    for direction, new_head in options:
        score = distance_to(new_head, state["food"])       # closer to the food is better

        if level == "hard":
            future_body = [new_head] + snake["body"][:-1]
            if count_open_cells(state, future_body, new_head) < len(future_body):
                score += 1000                              # not enough room: a dead end

        if best_score is None or score < best_score:
            best_score = score
            best_direction = direction
    return best_direction
