import argparse
import curses
import logging
import sys

from powerranger.view import View, Cursor

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

    if char == ord("q"):
        _log.info("Exiting peacfully.")
        sys.exit()

def curses_main(stdscr):
    """Program entry point."""
    parser = argparse.ArgumentParser(description="A ranger-inspired file manager for PowerShell.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
    args = parser.parse_args()

    if args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    if args.verbose > 0:
        logging.basicConfig(level=logging.INFO)

    curses.curs_set(Cursor.HIDDEN)

    while True:
        View(stdscr).render()

        try:
            handle_input()
        except SystemExit:
            break


def main():
    """Console script entry point."""
    curses.wrapper(curses_main)


if __name__ == "__main__":
    main()
