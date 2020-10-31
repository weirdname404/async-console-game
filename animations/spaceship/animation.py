from itertools import cycle
from core.objects import SpaceShip
from core.event_loop import Sleep
from core.types import Animation
from utils.curses_tools import get_frame_size

with open('animations/spaceship/rocket_frame_1.txt', 'r') as f:
    ROCKET_FRAME_1 = f.read()

with open('animations/spaceship/rocket_frame_2.txt', 'r') as f:
    ROCKET_FRAME_2 = f.read()

# animation should change every 2 tics
SPACESHIP_ANIMATION: Animation = (
    (2, ROCKET_FRAME_1),
    (2, ROCKET_FRAME_2)
)
FRAME_WIDTH, FRAME_HEIGHT = get_frame_size(ROCKET_FRAME_1)


async def animate_spaceship():
    ship = SpaceShip()
    for tics, frame in cycle(SPACESHIP_ANIMATION):
        ship.frame = frame
        await Sleep(tics)
