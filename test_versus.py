# test_versus.py - quick checks for versus_mode.py and ai_player.py. Needs no window.
# Run with:  python3 test_versus.py

import game_engine as engine
import versus_mode
import ai_player
from config import GRID_MAX


def make_state(mode="multi", level="medium"):
    """A running two-snake game. Tests then place the snakes exactly where they want."""
    state = engine.new_game_state()
    versus_mode.start_mode(state, mode, level)
    state["status"] = "running"
    return state, state["snakes"][0], state["snakes"][1]


def place(snake, body, direction):
    snake["body"] = body
    snake["direction"] = direction
    snake["next_direction"] = direction


def test_multi_creates_two_human_snakes():
    state, one, two = make_state("multi")
    assert len(state["snakes"]) == 2
    assert one["controller"] == "human" and two["controller"] == "human"


def test_ai_mode_creates_ai_snake():
    state, you, ai = make_state("ai", "hard")
    assert you["controller"] == "human" and ai["controller"] == "ai"
    assert state["ai_level"] == "hard"
    assert state["food"] not in you["body"] + ai["body"]


def test_key_groups():
    state, one, two = make_state("multi")
    assert versus_mode.snake_for_keys(state, "wasd") is one
    assert versus_mode.snake_for_keys(state, "arrows") is two
    state, you, ai = make_state("ai")
    assert versus_mode.snake_for_keys(state, "wasd") is you
    assert versus_mode.snake_for_keys(state, "arrows") is you


def test_waits_for_every_human():
    state, one, two = make_state("multi")
    one["next_direction"] = "right"            # P1 pressed a key, P2 did not
    versus_mode.update_versus(state)
    assert one["body"] == [(-8, 0)] and two["body"] == [(8, 0)]


def test_snakes_pass_through_each_other():
    state, one, two = make_state("multi")
    place(one, [(0, 0)], "right")
    place(two, [(1, 1), (1, 0), (1, -1)], "up")   # one's next cell is part of two's body
    state["food"] = (9, 9)
    versus_mode.update_versus(state)
    assert one["alive"] and two["alive"] and state["status"] == "running"
    assert one["body"][0] == (1, 0)


def test_both_eat_same_food_share_it():
    state, one, two = make_state("multi")
    place(one, [(0, 0)], "right")
    place(two, [(2, 0)], "left")
    state["food"] = (1, 0)
    versus_mode.update_versus(state)
    assert one["score"] == 10 and two["score"] == 10
    assert len(one["body"]) == 2 and len(two["body"]) == 2
    assert state["food"] not in one["body"] + two["body"]
    assert state["status"] == "running"


def test_wall_death_means_the_other_wins():
    state, one, two = make_state("multi")
    place(one, [(GRID_MAX, 0)], "right")
    place(two, [(0, 5)], "right")
    state["food"] = (9, 9)
    versus_mode.update_versus(state)
    assert state["status"] == "game_over" and state["result"] == "P2 WINS!"


def test_both_die_same_step_is_a_draw():
    state, one, two = make_state("multi")
    place(one, [(GRID_MAX, 0)], "right")
    place(two, [(-GRID_MAX, 5)], "left")
    state["food"] = (9, 9)
    versus_mode.update_versus(state)
    assert state["status"] == "game_over" and state["result"] == "DRAW!"


def test_you_win_message_against_ai():
    state, you, ai = make_state("ai")
    place(you, [(0, 0)], "right")
    place(ai, [(GRID_MAX, 0)], "right")
    state["obstacles"] = [(GRID_MAX, 1), (GRID_MAX, -1)]   # the AI is trapped: wall ahead, obstacles beside
    state["food"] = (9, 9)
    versus_mode.update_versus(state)
    assert state["result"] == "YOU WIN!"


def test_ai_goes_for_the_food():
    state, you, ai = make_state("ai", "hard")
    place(ai, [(0, 0)], "up")
    state["food"] = (5, 0)
    assert ai_player.choose_ai_direction(state, ai, "hard") == "right"


def test_ai_avoids_obstacles_and_walls():
    state, you, ai = make_state("ai", "hard")
    place(ai, [(0, 0)], "right")
    state["obstacles"] = [(1, 0)]
    state["food"] = (5, 0)                     # the obstacle is between the AI and the food
    assert ai_player.choose_ai_direction(state, ai, "hard") != "right"
    place(ai, [(GRID_MAX, 0)], "right")
    state["obstacles"] = []
    assert ai_player.choose_ai_direction(state, ai, "hard") != "right"


def test_ai_survives_a_long_game_on_hard():
    for trial in range(5):
        state = engine.new_game_state()
        snake = state["snakes"][0]
        snake["controller"] = "ai"
        place(snake, [(0, 0)], "right")
        for step in range(500):
            snake["next_direction"] = ai_player.choose_ai_direction(state, snake, "hard")
            engine.update_game(state)
            assert snake["alive"], f"AI died on step {step} in trial {trial}"


if __name__ == "__main__":
    tests = [value for name, value in list(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"\nAll {len(tests)} tests passed.")
