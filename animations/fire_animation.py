import curses
from core.event_loop import Sleep
from config import LASER_SPEED
from core.obstacles import obstacle_manager
from core.types import Coordinate, Animation

shot_animation: Animation = (
    (1, '*'),
    (1, '0')
)


async def animate_gunshot(canvas,
                          pos: Coordinate,
                          velocity=None):
    """Draws animation of gun shot, direction and speed can be specified."""

    x, y = map(round, pos)
    if velocity is None:
        vel_x, vel_y = 0, -LASER_SPEED
    else:
        vel_x, vel_y = velocity

    for tics, frame in shot_animation:
        canvas.addstr(y, x, frame)
        await Sleep(tics)
    # clear last frame of shot animation
    canvas.addstr(y, x, ' ')

    x += vel_x
    y += vel_y

    symbol = '-' if vel_x else '|'

    height, width = canvas.getmaxyx()
    max_y, max_x = height - 1, width - 1

    curses.beep()

    while 0 < y < max_y and 0 < x < max_x:
        for obstacle in obstacle_manager.get_front_objects(x):
            if obstacle.has_collision((x, y)):
                obstacle.terminate()
                return
        canvas.addstr(round(y), round(x), symbol)
        await Sleep(1)
        canvas.addstr(round(y), round(x), ' ')
        x += vel_x
        y += vel_y
