import curses
import inspect
from typing import Dict


class Colors:
    """Wrapper around curses colors for Items."""
    _pairs: Dict[str, int] = {}

    @classmethod
    def blue_on_black(cls) -> curses.color_pair:
        """Initialized color pair."""
        func = inspect.getframeinfo(inspect.currentframe()).function
        return cls._setup_pair(func, curses.COLOR_BLUE, curses.COLOR_BLACK)

    @classmethod
    def white_on_blue(cls) -> curses.color_pair:
        """Initialized color pair."""
        func = inspect.getframeinfo(inspect.currentframe()).function
        return cls._setup_pair(func, curses.COLOR_WHITE, curses.COLOR_BLUE)

    @classmethod
    def black_on_white(cls) -> curses.color_pair:
        """Initialized color pair."""
        func = inspect.getframeinfo(inspect.currentframe()).function
        return cls._setup_pair(func, curses.COLOR_BLACK, curses.COLOR_WHITE)

    @classmethod
    def yellow_on_black(cls) -> curses.color_pair:
        """Initialized color pair."""
        func = inspect.getframeinfo(inspect.currentframe()).function
        return cls._setup_pair(func, curses.COLOR_YELLOW, curses.COLOR_BLACK)

    @classmethod
    def default(cls) -> curses.color_pair:
        """Initialized color pair."""
        func = inspect.getframeinfo(inspect.currentframe()).function
        return cls._setup_pair(func, curses.COLOR_WHITE, curses.COLOR_BLACK)

    @classmethod
    def _setup_pair(cls, pair_name, foreground, background):
        """Lazily configure and remember an ncurses color pair."""
        if cls._pairs.get(pair_name) is None:
            if not cls._pairs:
                cls._pairs[pair_name] = 1
            else:
                cls._pairs[pair_name] = max(cls._pairs.values()) + 1

            curses.init_pair(cls._pairs[pair_name], foreground, background)

        return curses.color_pair(cls._pairs[pair_name])
