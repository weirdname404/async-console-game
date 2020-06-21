import time
import curses
import asyncio
import random
from typing import List, Tuple, Generator

Animation = List[Tuple[int, int]]
Coordinate = Tuple[int, int]

# in seconds
TIC_TIMEOUT = 0.1
STARS = '+*.:'

# (TICs, State)
STAR_ANIMATION: Animation = [
    (20, curses.A_DIM),
    (3, curses.A_NORMAL),
    (5, curses.A_BOLD),
    (3, curses.A_NORMAL)
]
DEFAULT_STAR_DENSITY = 0.1


def shift_animation(animation: Animation) -> Generator[Animation, None, None]:
    """
    Shifts first tick of animation sequence to the end
    """
    while True:
        init_ticks, init_state = animation[0]

        if init_ticks - 1 == 0:
            animation = animation[1:]
        else:
            animation[0] = (init_ticks - 1, init_state)

        if init_state != animation[-1][1]:
            animation.append((0,0))

        last_ticks, _ = animation[-1]
        animation[-1] = (last_ticks + 1, init_state)

        yield animation.copy()


def get_random_xy(max_y: int, max_x: int, density: float = None) -> Generator[Coordinate, None, None]:
    used_xy = set()
    density = DEFAULT_STAR_DENSITY if density is None else density

    for _ in range(int(max_x * max_y * density)):
        x_y = random.randint(1, max_x - 2), random.randint(1, max_y - 2)

        if x_y in used_xy:
            continue

        used_xy.add(x_y)
        yield x_y


class Sleep:
    def __await__(self):
        return (yield self)

    def __init__(self, seconds):
        self.seconds = seconds


async def sleep(amount_of_ticks):
    for _ in range(amount_of_ticks):
        await Sleep(TIC_TIMEOUT)


async def draw_star(canvas, row: int, column: int, star: str, animation: Animation):
    while True:
        for ticks, state in animation:
            canvas.addstr(row, column, star, state)
            await sleep(ticks)


def main(canvas):
    canvas.border()
    curses.curs_set(False)
    coroutines = []
    animation_shifter = shift_animation(STAR_ANIMATION)

    for x, y in get_random_xy(*canvas.getmaxyx()):
        coroutines.append(
            draw_star(
                canvas=canvas,
                row=y,
                column=x,
                star=random.choice(STARS),
                animation=next(animation_shifter)
            )
        )

    start_event_loop(coroutines, canvas)


def start_event_loop(coroutines, canvas):
    while True:
        for c in coroutines:
            clock: Sleep = c.send(None)

        canvas.refresh()
        time.sleep(clock.seconds)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)
