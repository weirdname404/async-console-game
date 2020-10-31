from utils import Singleton


class SpaceShip(metaclass=Singleton):
    __slots__ = (
        'max_speed', 'fire_cooldown', 'frame'
    )
