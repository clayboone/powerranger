import curses
import itertools
import os
from pathlib import Path
from typing import Dict, Optional, Union

DEFAULT_STARTUP_DIR = os.curdir
SORT_FOLDERS_ON_TOP = True


class Colors:
    """Wrapper around curses colors for Items."""
    _pairs: Dict[str, int] = {}

    @classmethod
    def blue_on_black(cls):
        """Initialized blue-on-black color pair."""
        return cls._setup_pair("blue_black", curses.COLOR_BLUE, curses.COLOR_BLACK)

    @classmethod
    def yellow_on_black(cls):
        """Initialized yellow-on-black color pair."""
        return cls._setup_pair("yellow_black", curses.COLOR_YELLOW, curses.COLOR_BLACK)

    @classmethod
    def default(cls):
        """Initialized white-on-black color pair."""
        return cls._setup_pair("default", curses.COLOR_WHITE, curses.COLOR_BLACK)

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


class Item:
    """An item inside of a Directory."""
    def __init__(self, path: Union[Path, str]):
        self._path = Path(path)

    @property
    def name(self) -> str:
        """The name of the item, not including parents."""
        return self._path.name

    @property
    def color(self):
        """An initialized ncurses color pair associated with the type of file
        for this Item.
        """
        if self._path.is_dir():
            return Colors.blue_on_black() | curses.A_BOLD

        return Colors.default()


class Directory:
    """A list of items inside of a directory."""
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)

    def __iter__(self):
        items = self.path.iterdir()

        if SORT_FOLDERS_ON_TOP:
            items1, items2 = itertools.tee(items)
            items = itertools.chain(
                (item for item in items1 if item.is_dir()),
                (item for item in items2 if not item.is_dir()),
            )

        for item in items:
            yield Item(item)


def resize_window(win):
    """Handler for a KEY_RESIZE event."""
    max_y, max_x = win.getmaxyx()
    curses.resize_term(max_y, max_x)
    win.clear()
    win.refresh()


def render_view(win, active_dir: Optional[Path]):
    """Create the main window view based on which Directory is active."""
    indent = 2
    offset_y = 1

    active_dir = active_dir or Path(DEFAULT_STARTUP_DIR)
    parent_dir = active_dir.absolute().parent

    for index, item in enumerate(Directory(parent_dir)):
        if index >= curses.LINES - offset_y - 1:
            break

        win.addnstr(index, indent, item.name, 100, item.color)


def handle_input(win) -> bool:
    """Wait for user input and handle the returned key."""
    char = win.getch()

    if char == curses.KEY_RESIZE:
        resize_window(win)

    win.addstr(curses.LINES - 3, 0, "-" * curses.COLS)
    win.addnstr(curses.LINES - 2, 0, f":{char}", 20)

    if char == ord("q"):
        return False

    return True


def main(win):
    """Program entry point."""
    curses.curs_set(0)
    active_dir = None

    while True:
        render_view(win, active_dir)

        if not handle_input(win):
            break


if __name__ == "__main__":
    curses.wrapper(main)
