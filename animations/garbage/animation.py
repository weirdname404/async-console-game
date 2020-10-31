from glob import glob
from utils.curses_tools import draw_frame
from animations.explosion import animate_explosion
from core.obstacles import obstacle_manager
from core.event_loop import Sleep, GameLoop

GARBAGE_FRAMES = []

for file_name in glob("animations/garbage/*.txt"):
    with open(file_name, 'r') as f:
        GARBAGE_FRAMES.append(f.read())


async def animate_garbage(canvas, garbage, velocity=0.6):
    """Animate garbage, flying from top to bottom.
    Сolumn position will stay same, as specified on start."""
    window_height, window_width = canvas.getmaxyx()

    x = min(max(garbage.x, 0), window_width - 1)
    y = garbage.y
    obstacle_manager.add_object(garbage)
    frame = garbage.frame

    try:
        while y < window_height:
            if garbage.term:
                raise Exception
            draw_frame(canvas, x, y, frame)
            await Sleep(0)
            draw_frame(canvas, x, y, frame, negative=True)
            y += velocity
            garbage.y = y
    except Exception:
        GameLoop().add_coroutine(
            animate_explosion(canvas, garbage.get_center_pos())
        )
        return

    finally:
        obstacle_manager.remove_object(garbage.uid)
