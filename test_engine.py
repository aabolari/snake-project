# test_engine.py - quick checks for game_engine.py. Needs no window.
# Run with:  python3 test_engine.py

import game_engine as engine
from config import GRID_MIN, GRID_MAX


def make_state(body, direction="right", food=(9, 9)):
    """A game state with the snake and food placed exactly where we want."""
    state = engine.new_game_state()
    snake = state["snakes"][0]
    snake["body"] = body
    snake["direction"] = direction
    snake["next_direction"] = direction
    state["food"] = food
    return state, snake


def test_movement():
    state, snake = make_state([(0, 0)])
    engine.update_game(state)
    assert snake["body"] == [(1, 0)]


def test_waits_before_first_key():
    state = engine.new_game_state()
    engine.update_game(state)
    assert state["snakes"][0]["body"] == [(0, 0)]


def test_no_reverse():
    state, snake = make_state([(0, 0)], direction="right")
    engine.change_direction(snake, "left")
    assert snake["next_direction"] == "right"


def test_two_quick_keys_cannot_reverse():
    state, snake = make_state([(2, 0), (1, 0), (0, 0)], direction="right")
    engine.change_direction(snake, "up")
    engine.change_direction(snake, "left")      # would reverse after "up" if unchecked
    engine.update_game(state)
    assert snake["alive"] and snake["direction"] == "up"


def test_eating_grows_and_scores():
    state, snake = make_state([(0, 0)], food=(1, 0))
    engine.update_game(state)
    assert len(snake["body"]) == 2
    assert snake["score"] == 10 and state["high_score"] == 10
    assert state["food"] not in snake["body"]


def test_wall_collision():
    state, snake = make_state([(GRID_MAX, 0)], direction="right")
    engine.update_game(state)
    assert not snake["alive"] and state["status"] == "game_over"


def test_self_collision():
    state, snake = make_state(
        [(2, 1), (2, 2), (1, 2), (1, 1), (1, 0)], direction="left")
    engine.update_game(state)
    assert not snake["alive"]


def test_tail_cell_is_safe():
    state, snake = make_state([(1, 0), (1, 1), (0, 1), (0, 0)], direction="left")
    engine.update_game(state)
    assert snake["alive"]


def test_food_never_on_snake():
    state = engine.new_game_state()
    snake = state["snakes"][0]
    all_cells = [(x, y) for x in range(GRID_MIN, GRID_MAX + 1)
                 for y in range(GRID_MIN, GRID_MAX + 1)]
    all_cells.remove((3, 3))
    snake["body"] = all_cells
    assert engine.spawn_food(state) == (3, 3)


def test_pause_and_restart():
    state, snake = make_state([(0, 0)], food=(1, 0))
    engine.update_game(state)                   # score 10
    engine.toggle_pause(state)
    assert state["status"] == "paused"
    engine.toggle_pause(state)
    assert state["status"] == "running"
    engine.reset_game(state)
    new_snake = state["snakes"][0]
    assert new_snake["score"] == 0 and new_snake["body"] == [(0, 0)]
    assert state["high_score"] == 10            # high score survives restart
    assert state["status"] == "running"


if __name__ == "__main__":
    tests = [value for name, value in list(globals().items()) if name.startswith("test_")]
    for test in tests:
        test()
        print("PASS", test.__name__)
    print(f"\nAll {len(tests)} tests passed.")
