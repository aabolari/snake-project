# versus_mode.py - the rules for the two-snake modes.
#   "multi" = 1v1 human (P1 uses WASD, P2 uses the arrow keys)
#   "ai"    = human vs AI
#
# RULES (agreed by the team):
#   - Snakes pass THROUGH each other. Only walls, your own body and obstacles kill you.
#   - If both snakes reach the food on the same step, both score and both grow.
#   - The first snake to die ends the game and the survivor wins.
#     If both die on the same step it is a draw.
#
# This file reuses the helper functions from game_engine.py, and
# single player (update_game in game_engine.py) is not touched at all.

import game_engine
from ai_player import choose_ai_direction
from config import P1_START, P2_START, POINTS_PER_FOOD


def start_mode(state, mode, ai_level="medium"):
    """Set up the snakes for the chosen mode. Single player needs no changes."""
    state["mode"] = mode
    if mode == "single":
        return

    if mode == "multi":
        state["snakes"] = [
            game_engine.create_snake("P1", P1_START, "human"),
            game_engine.create_snake("P2", P2_START, "human"),
        ]
    elif mode == "ai":
        ai_snake = game_engine.create_snake("AI", P2_START, "ai")
        ai_snake["direction"] = "left"          # the AI is already moving toward you
        ai_snake["next_direction"] = "left"
        state["snakes"] = [game_engine.create_snake("YOU", P1_START, "human"), ai_snake]
        state["ai_level"] = ai_level

    state["result"] = None
    state["food"] = game_engine.spawn_food(state)   # the old food may sit on a new snake


def snake_for_keys(state, keys):
    """Which snake does this key group steer? keys is "wasd" or "arrows"."""
    if state["mode"] == "multi":
        if keys == "wasd":
            return state["snakes"][0]
        return state["snakes"][1]
    return state["snakes"][0]       # single player and vs AI: both groups steer the human


def all_humans_ready(state):
    """True once every human snake has been given a first direction."""
    for snake in state["snakes"]:
        if snake["controller"] == "human" and snake["next_direction"] == "stop":
            return False
    return True


def plan_move(state, snake):
    """Work out what one snake WANTS to do this step, without changing the board yet.

    Returns three things: the new head cell, whether the snake is growing
    (it reaches the food) and whether it dies. Planning every snake first
    and moving them afterwards keeps the step fair: nobody gets to move
    before the other one.
    """
    snake["direction"] = snake["next_direction"]
    new_head = game_engine.get_next_head(snake)
    growing = (new_head == state["food"])
    dies = (game_engine.check_wall_collision(new_head)
            or game_engine.check_self_collision(snake, new_head, growing)
            or game_engine.check_obstacle_collision(state, new_head))
    return new_head, growing, dies


def result_text(winner):
    """The message for the winning snake, for example "P1 WINS!"."""
    if winner["name"] == "YOU":
        return "YOU WIN!"
    return winner["name"] + " WINS!"


def decide_winner(state):
    """Check whether the game is over after a step, and set state["result"]."""
    snakes = state["snakes"]
    alive = [snake for snake in snakes if snake["alive"]]

    if len(alive) == len(snakes) and state["food"] is not None:
        return                                  # everybody is alive: the game goes on

    state["status"] = "game_over"
    if len(alive) == 1:
        state["result"] = result_text(alive[0])
    elif len(alive) == 0:
        state["result"] = "DRAW!"               # both died on the same step
    else:                                       # board completely full: highest score wins
        first, second = snakes[0], snakes[1]
        if first["score"] == second["score"]:
            state["result"] = "DRAW!"
        elif first["score"] > second["score"]:
            state["result"] = result_text(first)
        else:
            state["result"] = result_text(second)


def update_versus(state):
    """Advance a two-snake game by one step. Order: wait, steer, plan, move, eat, decide."""
    if not all_humans_ready(state):
        return                                  # everybody waits for the humans' first key

    snakes = state["snakes"]

    # Phase 1: the AI chooses, then every snake plans its move.
    plans = []
    for snake in snakes:
        if snake["controller"] == "ai":
            snake["next_direction"] = choose_ai_direction(state, snake, state["ai_level"])
        plans.append(plan_move(state, snake))

    # Phase 2: carry out the plans.
    food_eaten = False
    for i in range(len(snakes)):
        new_head, growing, dies = plans[i]
        if dies:
            snakes[i]["alive"] = False
            continue
        game_engine.move_snake(snakes[i], new_head, growing)
        if growing:
            snakes[i]["score"] += POINTS_PER_FOOD     # both score if both reach it together
            state["high_score"] = max(state["high_score"], snakes[i]["score"])
            food_eaten = True

    if food_eaten:
        state["food"] = game_engine.spawn_food(state)  # spawned once, after every snake has moved

    decide_winner(state)
