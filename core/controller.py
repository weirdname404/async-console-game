from animations.spaceship.animation import FRAME_HEIGHT, FRAME_WIDTH
from animations.fire_animation import animate_gunshot
from animations.explosion import animate_explosion
from core.objects import spaceship, Game
from core.obstacles import obstacle_manager
from core.physics import update_velocity
from core.event_loop import Sleep, GameLoop
from core.events import show_gameover
from config import SPACESHIP_MAX_X_SPEED, SPACESHIP_MAX_Y_SPEED
from utils.curses_tools import read_controls, clean_draw, draw_frame

SPACESHIP_X_HALF = FRAME_WIDTH // 2
SPACESHIP_Y_HALF = FRAME_HEIGHT // 2


async def run_spaceship(canvas, x, y):
    """
    Spaceship coroutine that handles player's input and draws frames.
    Works every step of event loop.
    """
    # getmaxyx() return height and width of the window.
    height, width = canvas.getmaxyx()
    # we want to stop the spaceship right before the border line
    max_x = width - FRAME_WIDTH - 1
    max_y = height - FRAME_HEIGHT - 1
    prev_frame = None
    game_loop = GameLoop()
    game = Game()
    vel_x, vel_y = 0, 0

    while True:
        # get current frame
        frame = spaceship.frame
        # read controls
        dy, dx, space = read_controls(canvas)
        if space and game.is_gun_available():
            # TODO add fire cooldown
            game_loop.add_coroutine(
                animate_gunshot(
                    canvas=canvas,
                    pos=(x + SPACESHIP_X_HALF, y - 1)
                )
            )
        vel_x, vel_y = update_velocity(
            x_direction=dx,
            y_direction=dy,
            velocity_vec=(vel_x, vel_y),
            velocity_limit_vec=(SPACESHIP_MAX_X_SPEED, SPACESHIP_MAX_Y_SPEED)
        )

        # count next coordinates
        # check borders intersection
        # choose closest point to the border
        x1 = max(1, min(x + vel_x, max_x))
        y1 = max(1, min(y + vel_y, max_y))
        # clean prev frame at old pos and draw current frame at new pos
        clean_draw(canvas, (x, y), (x1, y1), prev_frame, frame)
        x, y = x1, y1

        # check collisions with obstacles
        for obstacle in obstacle_manager.get_front_objects(x, x + FRAME_WIDTH):
            # GAME OVER
            if obstacle.has_collision(obj_pos=(x, y),
                                      obj_size=(FRAME_WIDTH, FRAME_HEIGHT)):
                game.over()
                # clear last spaceship frame
                draw_frame(canvas, x, y, frame, True)
                spaceship_center_pos = (
                    x + SPACESHIP_X_HALF,
                    y + SPACESHIP_Y_HALF
                )
                game_loop.add_coroutine(
                    animate_explosion(canvas=canvas,
                                      center_pos=spaceship_center_pos)
                )
                game_loop.add_coroutine(
                    show_gameover(canvas)
                )
                return

        await Sleep(0)
        prev_frame = frame
