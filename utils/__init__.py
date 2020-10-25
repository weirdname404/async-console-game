from typing import Generator
from game_types import Animation


def shift_animation(animation: Animation) -> Generator[Animation, None, None]:
    """
    Shifts first tic of animation sequence to the end
    """
    animation = list(animation)
    while True:
        init_tics, init_state = animation[0]

        if init_tics - 1 == 0:
            animation = animation[1:]
        else:
            animation[0] = (init_tics - 1, init_state)

        if init_state != animation[-1][1]:
            animation.append((0, 0))

        last_tics, _ = animation[-1]
        animation[-1] = (last_tics + 1, init_state)

        yield tuple(animation.copy())


class Singleton(type):
    isinstances = {}

    def __call__(cls, *args, **kwargs):
        if cls.isinstances.get(cls) is None:
            cls.isinstances[cls] = super().__call__(*args, **kwargs)
        return cls.isinstances[cls]
