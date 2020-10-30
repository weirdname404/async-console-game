import random
from config import GARBAGE_SPAWN_COOLDOWN as gsc
from core.obstacles import Obstacle
from core.event_loop import GameLoop, Sleep
from animations.garbage.animation import animate_garbage, GARBAGE_FRAMES


async def fill_orbit_with_garbage(canvas, cooldown=gsc):
    '''Garbage spawner'''
    _, width = canvas.getmaxyx()
    game_loop = GameLoop()
    cnt = 1
    while True:
        x, y = random.randint(1, width), 0
        game_loop.add_coroutine(
            animate_garbage(
                canvas=canvas,
                garbage=Obstacle(
                    pos=(x, y),
                    frame=random.choice(GARBAGE_FRAMES),
                    uid=cnt
                )
            )
        )
        cnt += 1
        await Sleep(cooldown)
