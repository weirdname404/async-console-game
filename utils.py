import random
import config
from typing import List, Tuple, Generator
from _types import Animation, Coordinate


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
    density = config.STAR_DENSITY if density is None else density

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
        await Sleep(config.TIC_TIMEOUT)
