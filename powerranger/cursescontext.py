"""Context managers for creating and pausing curses windows."""
from contextlib import contextmanager
import curses
import logging

from view import View

_log = logging.getLogger(__name__)  # pylint: disable=invalid-name


@contextmanager
def start() -> curses.newwin:
    """Context manager yielding a new curses session."""
    _log.debug("Enabling curses")
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    if curses.has_colors():
        curses.start_color()

    try:
        yield stdscr

    except Exception:
        _log.debug("Unhandled exception during a curses screen")
        raise

    finally:
        _log.debug("Disabling curses")
        curses.echo()
        curses.nocbreak()
        curses.endwin()


@contextmanager
def pause():
    """Context manager to disable curses and re-enable upon leaving."""
    _log.debug("Pausing curses")
    curses.echo()
    curses.nocbreak()
    curses.endwin()

    try:
        yield

    except Exception:
        _log.debug("Unhandled exception while curses was paused")
        raise

    else:
        _log.debug("Re-enabling curses")
        stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        stdscr.keypad(True)

        if curses.has_colors():
            curses.start_color()

        View(stdscr).render()
