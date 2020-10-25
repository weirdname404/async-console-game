import random
from glob import glob
from utils.curses_tools import draw_frame
from core.event_loop import Sleep, GameLoop

GARBAGE = []

for file_name in glob("animations/garbage/*.txt"):
    with open(file_name, 'r') as f:
        GARBAGE.append(f.read())


async def spawn_garbage(canvas, column, garbage_frame, speed=1):
    """Animate garbage, flying from top to bottom.
    Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = min(max(column, 0), columns_number - 1)
    row = 0

    while row < rows_number:
        draw_frame(canvas, row, column, garbage_frame)
        await Sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed


async def fill_orbit_with_garbage(canvas, cooldown=10):
    '''Garbage spawner'''
    _, columns_number = canvas.getmaxyx()
    gl = GameLoop()
    while True:
        gl.add_coroutine(
            spawn_garbage(
                canvas=canvas,
                column=random.randint(1, columns_number),
                garbage_frame=random.choice(GARBAGE)
            )
        )
        await Sleep(cooldown)
