import curses
import random
from animations.star_animation import STAR_ANIMATION, animate_star
from animations.spaceship.animation import (
    animate_spaceship, FRAME_HEIGHT
)
from config import (
    STARS, BORDERS, TEXT_WINDOW_H,
    TEXT_WINDOW_W, START_Y_DELTA,
    START_YEAR
)
from core.controller import run_spaceship
from core.events import fill_orbit_with_garbage, show_game_progress
from core.event_loop import GameLoop
from core.objects import Game
from core.obstacles import show_obstacles
from utils import shift_animation
from utils.curses_tools import get_random_coordinate


def main(canvas):
    game = Game(START_YEAR)
    canvas.nodelay(1)
    curses.curs_set(False)

    height, width = canvas.getmaxyx()
    max_y, max_x = height - 1, width - 1
    text_window_pos = max_x - TEXT_WINDOW_W, max_y - TEXT_WINDOW_H

    # spaceship pos
    spaceship_x = max_x // 2
    spaceship_y = max_y - FRAME_HEIGHT - START_Y_DELTA

    animation_generator = shift_animation(STAR_ANIMATION)
    coroutines = []
    for x, y in get_random_coordinate(max_x, max_y):
        coroutines.append(
            animate_star(
                canvas=canvas,
                pos=(x, y),
                star=random.choice(STARS),
                animation=next(animation_generator)
            )
        )

    coroutines.extend(
        [
            animate_spaceship(),
            run_spaceship(canvas=canvas, x=spaceship_x, y=spaceship_y),
            game.increase_year(),
            fill_orbit_with_garbage(canvas),
            show_game_progress(canvas, *text_window_pos),
        ]
    )

    if BORDERS:
        coroutines.append(show_obstacles(canvas))

    GameLoop(coroutines, canvas).start()


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
