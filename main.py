# main.py - connects the pieces. Run the game with:  python3 main.py
#
#   keys (ui.py)  ->  handlers below  ->  rules (game_engine.py)
#   state         ->  ui.draw_game()  ->  what you see

import turtle
import config
import game_engine
import ui
import versus_mode

# The one shared game state. Every module reads and changes THIS dictionary.
state = game_engine.new_game_state()


# ----------------------------------------------------------------------
# Handlers: called by ui.bind_keys when a key is pressed
# ----------------------------------------------------------------------
def handle_direction(direction, keys):
    """keys says which key group was pressed: "wasd" or "arrows"."""
    if state["status"] == "running":
        player = versus_mode.snake_for_keys(state, keys)
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
        if state["mode"] == "single":
            game_engine.update_game(state)
        else:
            versus_mode.update_versus(state)
    ui.draw_game(state)
    turtle.ontimer(game_tick, config.TICK_MS)

# The three difficulty cards are drawn in the same three spots as the mode cards,
# so a click on the top card arrives here as "single", the middle one as "multi", etc.
DIFFICULTY_BY_CARD = {"single": "easy", "multi": "medium", "ai": "hard"}


def handle_menu_selection(choice):
    """Handle a click (or key 1/2/3) on the main menu or on the difficulty menu."""
    if state["status"] == "menu":
        if choice == "ai":
            state["status"] = "difficulty"      # ask Easy / Medium / Hard first
        else:
            versus_mode.start_mode(state, choice)
            state["status"] = "running"
    elif state["status"] == "difficulty":
        versus_mode.start_mode(state, "ai", DIFFICULTY_BY_CARD[choice])
        state["status"] = "running"

def run_game():
    ui.setup_ui()

    print(f"BOOT STATE: {state['status']}")

    ui.bind_keys(handle_direction, handle_spacebar, handle_restart, handle_menu_selection)
    game_tick()
    turtle.mainloop()


if __name__ == "__main__":
    run_game()
