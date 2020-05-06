import argparse
import curses
import logging
import subprocess
import sys

import config
from cursescontext import CursesContext
from view import View, Cursor

_log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def handle_input():
    """Wait for user input and handle the returned key."""
    char = View().stdscr.getch()

    if char == curses.KEY_RESIZE:
        View().resize()

    if char == ord("j"):
        View().active_item_index += 1

    if char == ord("k"):
        View().active_item_index -= 1

    if char == ord("h"):
        View().active_dir = View().active_dir.parent

    if char == ord("l"):
        if View().active_item.is_dir():
            View().active_dir = View().active_item
        else:
            _log.debug("Opening: %s", View().active_item)

            try:
                subprocess.check_call([config.EDITOR, View().active_item])
            except FileNotFoundError:
                _log.error("File not found: %s", config.EDITOR)
            except subprocess.CalledProcessError:
                _log.error("Process exited abnormally: %s", config.EDITOR)

    if char == ord("q"):
        _log.info("Exiting peacfully.")
        sys.exit()


def main(win):
    """Initialize View and wait for user input."""
    parser = argparse.ArgumentParser(description="A ranger-inspired file manager for PowerShell.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
    args = parser.parse_args()

    if args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    if args.verbose > 0:
        logging.basicConfig(level=logging.INFO)

    curses.curs_set(Cursor.HIDDEN)

    while True:
        View(win).render()

        try:
            handle_input()
        except SystemExit:
            break


if __name__ == "__main__":
    with CursesContext().curses_screen() as stdscr:
        main(stdscr)
