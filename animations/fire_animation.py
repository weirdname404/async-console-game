import curses
from core.event_loop import Sleep
from config import LASER_SPEED


async def animate_gunshot(
    canvas,
    y: int,
    x: int,
    rows_speed: int = -LASER_SPEED,
    columns_speed: int = 0
):
    """Display animation of gun shot, direction and speed can be specified."""

    row, column = y, x

    canvas.addstr(round(row), round(column), '*')
    await Sleep(2)

    canvas.addstr(round(row), round(column), 'O')
    await Sleep(2)
    canvas.addstr(round(row), round(column), ' ')

    row += rows_speed
    column += columns_speed

    symbol = '-' if columns_speed else '|'

    rows, columns = canvas.getmaxyx()
    max_row, max_column = rows - 1, columns - 1

    curses.beep()

    while 0 < row < max_row and 0 < column < max_column:
        canvas.addstr(round(row), round(column), symbol)
        await Sleep(1)
        canvas.addstr(round(row), round(column), ' ')
        row += rows_speed
        column += columns_speed
