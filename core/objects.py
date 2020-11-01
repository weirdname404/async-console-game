from utils import Singleton
from core.event_loop import Sleep

PHRASES = {
    1957: "First Sputnik",
    1961: 'Gagarin: "Let\'s go!"',
    1969: 'Armstrong landed on the moon.',
    1971: "First orbital space station Salute-1",
    1981: "Flight of the Shuttle Columbia",
    1998: 'ISS was launched',
    2011: 'The first orbital image of Mercury',
    2020: "Take the plasma gun! Shoot the garbage!",
}


class Game(metaclass=Singleton):
    __slots__ = ('text', 'year', 'is_over')

    def __init__(self, year):
        self.year = year
        self.text = ''
        self.is_over = False

    def over(self):
        self.is_over = True

    def is_gun_available(self):
        if self.year >= 2020:
            return True
        return False

    async def increase_year(self):
        while True:
            if self.is_over:
                return
            self.year += 1
            if (text := PHRASES.get(self.year)) is not None:
                self.text = text
            # year increases every 1.5 secs
            await Sleep(15)

    def get_garbage_delay_tics(self):
        if self.year < 1961:
            return None
        elif self.year < 1969:
            return 20
        elif self.year < 1981:
            return 14
        elif self.year < 1995:
            return 10
        elif self.year < 2010:
            return 8
        elif self.year < 2020:
            return 6
        else:
            return 2


class SpaceShip(metaclass=Singleton):
    __slots__ = (
        'max_speed', 'fire_cooldown', 'frame'
    )
