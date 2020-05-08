import argparse
import curses
import logging
import subprocess

import config
from view import View, Cursor, start_curses, stop_curses

_log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def handle_input() -> str:
    """Wait for user input and handle the returned key.

    @return Errors.
    """
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
            View().active_dir = View().active_item.resolve()
        else:
            if config.PAUSE_ON_OPENING_FILE:
                stop_curses()

            call_editor()
            start_curses()

    if char == ord("q"):
        _log.info("Exiting peacfully.")
        return "ok"

    return None


def call_editor():
    """Call the text editor."""
    _log.debug('Calling: "%s" with "%s"', config.EDITOR, View().active_item)

    try:
        subprocess.check_call([config.EDITOR, View().active_item])

    except FileNotFoundError:
        _log.error("File not found: %s", config.EDITOR)

    except subprocess.CalledProcessError:
        _log.error("Process exited abnormally: %s", config.EDITOR)


def main():
    """Initialize View and wait for user input."""
    parser = argparse.ArgumentParser(description="A ranger-inspired file manager for PowerShell.")
    parser.add_argument("-v", "--verbose", action="count", default=0, help="increase output verbosity")
    args = parser.parse_args()

    if args.verbose > 1:
        logging.basicConfig(level=logging.DEBUG)
    if args.verbose > 0:
        logging.basicConfig(level=logging.INFO)

    start_curses()
    curses.curs_set(Cursor.HIDDEN)

    while True:
        View().render()
        err = handle_input()

        if err:
            stop_curses()
            _log.info("Exit reason: %s", err)
            break


if __name__ == "__main__":
    main()
