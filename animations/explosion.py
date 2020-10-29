import curses
from utils.curses_tools import draw_frame, get_frame_size
from core.event_loop import Sleep
from core.types import Animation

EXPLOSION_FRAMES = [
    """
    (_)
 (  (   (  (
() (  (  )
  ( )  ()
    """,
    """
    (_)
 (  (   (
   (  (  )
    )  (
    """,
    """
      (
    (   (
   (     (
    )  (
    """,
    """
      (
        (
     (
    """
]
EXPLOSION_FRAMES: Animation = tuple((0, frame) for frame in EXPLOSION_FRAMES)


async def animate_explosion(canvas, center_pos):
    width, height = get_frame_size(EXPLOSION_FRAMES[0][1])
    center_x, center_y = center_pos
    corner_x = center_x - width // 2
    corner_y = center_y - height // 2

    curses.beep()
    for tics, frame in EXPLOSION_FRAMES:
        draw_frame(canvas, corner_y, corner_x, frame)
        await Sleep(tics)
        draw_frame(canvas, corner_y, corner_x, frame, negative=True)
        await Sleep(tics)
