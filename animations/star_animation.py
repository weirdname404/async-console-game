import curses
from core.event_loop import Sleep
from core.types import Animation, Coordinate

# (TICs, State)
STAR_ANIMATION: Animation = (
    (20, curses.A_DIM),
    (3, curses.A_NORMAL),
    (5, curses.A_BOLD),
    (3, curses.A_NORMAL)
)


async def animate_star(canvas,
                       pos: Coordinate,
                       star: str,
                       animation: Animation):
    x, y = pos
    while True:
        for tics, state in animation:
            canvas.addstr(y, x, star, state)
            await Sleep(tics)
