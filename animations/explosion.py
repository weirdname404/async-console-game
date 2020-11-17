import curses
from utils.curses_tools import draw_frame, get_frame_size
from core.event_loop import Sleep
from core.types import Animation, Coordinate

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


async def animate_explosion(canvas, center_pos: Coordinate):
    width, height = get_frame_size(EXPLOSION_FRAMES[0][1])
    corner_x = center_pos[0] - width // 2
    corner_y = center_pos[1] - height // 2

    curses.beep()
    for tics, frame in EXPLOSION_FRAMES:
        draw_frame(canvas, corner_x, corner_y, frame)
        await Sleep(tics)
        draw_frame(canvas, corner_x, corner_y,  frame, negative=True)
        await Sleep(tics)
