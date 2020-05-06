from contextlib import contextmanager
import curses
import logging

_log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class CursesContext:
    """Context managers for starting and stopping curses sessions."""

    def __init__(self):
        self.stdscr = None

    @contextmanager
    def curses_screen(self) -> curses.newwin:
        """Context manager yielding a new curses session."""
        _log.debug("Enabling curses")
        self.stdscr = curses.initscr()
        curses.cbreak()
        curses.noecho()
        self.stdscr.keypad(True)

        if curses.has_colors():
            curses.start_color()

        try:
            yield self.stdscr

        except Exception:
            _log.debug("Unhandled exception during a curses screen")
            raise

        finally:
            _log.debug("Disabling curses")
            curses.echo()
            curses.nocbreak()
            curses.endwin()
