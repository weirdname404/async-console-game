import time
import curses


def draw_star_animation(canvas, y, x, star):
    animation = [
        (2, curses.A_DIM),
        (0.3, curses.A_NORMAL),
        (0.5, curses.A_BOLD),
        (0.3, curses.A_NORMAL)
    ]

    for state in animation:
        t, style = state
        canvas.addstr(y, x, star, style)
        canvas.refresh()
        time.sleep(t)


def main(canvas):
    canvas.border()
    curses.curs_set(False)
    while True:
        draw_star_animation(canvas, 5, 20, "*")


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(main)