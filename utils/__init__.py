from typing import Generator
from _types import Animation


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
            animation.append((0, 0))

        last_ticks, _ = animation[-1]
        animation[-1] = (last_ticks + 1, init_state)

        yield animation.copy()
