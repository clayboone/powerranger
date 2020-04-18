import curses
import sys

from view import View, Cursor


def handle_input():
    """Wait for user input and handle the returned key."""
    char = View().stdscr.getch()

    if char == curses.KEY_RESIZE:
        View().resize()

    if char == ord("q"):
        sys.exit()


def main(stdscr):
    """Program entry point."""
    curses.curs_set(Cursor.HIDDEN)

    while True:
        View(stdscr).render()
        handle_input()


if __name__ == "__main__":
    curses.wrapper(main)
