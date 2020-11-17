import random
from animations.garbage.animation import animate_garbage, GARBAGE_FRAMES
from animations.screen import game_over_frame
from core.obstacles import Obstacle
from core.objects import Game
from core.event_loop import GameLoop, Sleep
from itertools import count
from utils.curses_tools import get_frame_size, draw_frame


async def fill_orbit_with_garbage(canvas, cooldown=None):
    '''Garbage spawner'''
    _, width = canvas.getmaxyx()
    game_loop = GameLoop()
    game = Game()
    # there should be no garbage in the very beginning
    while game.get_garbage_delay_tics() is None:
        await Sleep(1)

    for uid in count(1, 1):
        x, y = random.randint(1, width), 0
        obstacle = Obstacle(
            pos=(x, y),
            frame=random.choice(GARBAGE_FRAMES),
            uid=uid
        )
        game_loop.add_coroutine(
            animate_garbage(
                canvas=canvas,
                garbage=obstacle
            )
        )
        await Sleep(game.get_garbage_delay_tics())


async def show_gameover(canvas):
    '''Show game over in the center of the screen'''
    centet_y, center_x = map(lambda v: v // 2, canvas.getmaxyx())
    w, h = get_frame_size(game_over_frame)
    start_x = center_x - w // 2
    start_y = centet_y - h // 2

    # small pause
    await Sleep(10)

    while True:
        draw_frame(canvas, start_x, start_y, game_over_frame)
        await Sleep(1)


async def show_game_progress(canvas, x, y):
    game = Game()
    while True:
        text = f"{game.year}   {game.text}"
        draw_frame(canvas, x, y, text)
        await Sleep(1)
        draw_frame(canvas, x, y, text, True)
