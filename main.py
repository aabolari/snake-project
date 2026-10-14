# main.py - connects the pieces. Run the game with:  python3 main.py
#
#   keys (ui.py)  ->  handlers below  ->  rules (game_engine.py)
#   state         ->  ui.draw_game()  ->  what you see

import turtle
import config
import game_engine
import ui

# The one shared game state. Every module reads and changes THIS dictionary.
state = game_engine.new_game_state()


# ----------------------------------------------------------------------
# Handlers: called by ui.bind_keys when a key is pressed
# ----------------------------------------------------------------------
def handle_direction(direction):
    if state["status"] == "running":
        player = state["snakes"][0]
        game_engine.change_direction(player, direction)


def handle_spacebar():
    """Context-aware input: restarts if dead, pauses if alive."""
    if state["status"] == "game_over":
        game_engine.reset_game(state)
    else:
        game_engine.toggle_pause(state)


def handle_restart():
    game_engine.reset_game(state)


# ----------------------------------------------------------------------
# The game loop
# ----------------------------------------------------------------------
def game_tick():
    """One frame: update the rules (if running), draw, then schedule the next frame.

    We use ontimer instead of `while True` so the window stays responsive
    to keys and buttons between frames.
    """
    if state["status"] == "running":
        game_engine.update_game(state)
    ui.draw_game(state)
    turtle.ontimer(game_tick, config.TICK_MS)


def run_game():
    ui.setup_ui()
    ui.bind_keys(handle_direction, handle_spacebar, handle_restart)
    game_tick()
    turtle.mainloop()


if __name__ == "__main__":
    run_game()
