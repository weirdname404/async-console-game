import math
from typing import Tuple


def _apply_acceleration(velocity, vel_limit, forward=True):
    """Change velocity — accelerate or brake — according to force direction."""

    vel_limit = abs(vel_limit)
    vel_fraction = velocity / vel_limit

    # special function that helps to get a big delta if spaceship idles
    # which will lead to a fast launch of the spaceship
    # and small delta if ship is already moving fast
    delta = math.cos(vel_fraction) * 0.75

    if forward:
        result_vel = velocity + delta
    else:
        result_vel = velocity - delta

    # Let's limit value by min_value and max_value
    result_vel = max(-vel_limit, min(result_vel, vel_limit))

    # if speed is close to 0, spaceship stops
    if abs(result_vel) < 0.1:
        result_vel = 0

    return result_vel


def update_velocity(x_direction: int,
                    y_direction: int,
                    velocity_vec: Tuple[int, int],
                    velocity_limit_vec: Tuple = (2, 2),
                    fading: float = 0.8) -> Tuple[int, int]:
    """
    Smoothly updates speed to make controls more handy/responsive.
    Returns new velocity value (vel_x, vel_y)

    x_direction — is a force direction by x axis. Possible values:
       -1 — if force pulls left
       0  — if force has no effect
       1  — if force pulls right

    y_direction — is a force direction by y axis. Possible values:
       -1 — if force pulls up
       0  — if force has no effect
       1  — if force pulls down

    """

    if x_direction not in (-1, 0, 1):
        raise ValueError(
            f'Wrong x_direction value {x_direction}. Expects -1, 0 or 1.'
        )

    if y_direction not in (-1, 0, 1):
        raise ValueError(
            f'Wrong y_direction value {y_direction}. Expects -1, 0 or 1.'
        )

    if fading < 0 or fading > 1:
        raise ValueError(
            f'Wrong fading value {fading}. Expects float between 0 and 1.'
        )

    # velocity always fades away
    vel_x, vel_y = map(lambda v: v * fading, velocity_vec)
    vel_x_limit, vel_y_limit = map(abs, velocity_limit_vec)

    if y_direction != 0:
        vel_y = _apply_acceleration(
            vel_y, vel_y_limit, y_direction > 0
        )

    if x_direction != 0:
        vel_x = _apply_acceleration(
            vel_x, vel_x_limit, x_direction > 0
        )

    return vel_x, vel_y
