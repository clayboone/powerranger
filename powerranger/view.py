import curses
import logging
from pathlib import Path

import config
from files import Directory
from singleton import SingletonMeta

_log = logging.getLogger(__name__)  # pylint: disable=invalid-name


class Cursor:
    """Labels for curses' magic values for the cursor setting."""
    HIDDEN = 0
    VISIBLE = 1
    HIGHLY_VISIBLE = 2


class View(metaclass=SingletonMeta):
    """The view from the user's perspective.

    View is a singleton which can be called from anywhere with the only
    constraint that in its first invocation, it must be passed the
    _CursesWindow created by curses.initscr()
    """
    def __init__(self, stdscr=None):
        # Intellisense respects Python's privacy conventions, so we use
        # curses.newwin as a hack which returns curses._CursesWindow for code
        # completion.
        self.stdscr: curses.newwin = stdscr
        self.active_dir = Path(config.DEFAULT_STARTUP_DIR).resolve()
        self._active_item_index = 0
        self._max_cursor_index = None

    def render(self):
        """Render the main window view."""
        panes = []

        header_offset = self._draw_header()
        border_offset = int(config.View.draw_boxes)
        height = curses.LINES - header_offset

        parent_width = int(curses.COLS * config.View.parent_pane_width_percent)
        parent_start = 0
        panes.append(curses.newwin(height, parent_width, header_offset, parent_start))

        # Path.parent will return active_dir if it happens to be the root, so
        # use parents[0] instead.
        for index, item in enumerate(Directory(self.active_dir.parents[0])):
            if index >= height - (2 * border_offset):
                break

            item.selected = item.name == self.active_dir.name

            panes[0].addnstr(index + border_offset, border_offset, item.name, parent_width, item.color)

        active_width = int(curses.COLS * config.View.active_pane_width_percent)
        active_start = parent_start + parent_width
        panes.append(curses.newwin(height, active_width, header_offset, active_start))

        for index, item in enumerate(Directory(self.active_dir)):
            if index >= height - (2 * border_offset):
                break

            item.selected = index == self.active_item_index
            self._max_cursor_index = index

            panes[1].addnstr(index + border_offset, border_offset, item.name, active_width, item.color)

        content_width = curses.COLS - (parent_width + active_width)
        content_start = active_start + active_width
        panes.append(curses.newwin(height, content_width, header_offset, content_start))

        self.stdscr.refresh()

        for pane in panes:
            if config.View.draw_boxes:
                pane.box()

            pane.refresh()

    def _draw_header(self) -> int:
        """Draw the View's top text and line.

        @return The combined vertical offset
        """
        self.stdscr.addnstr(0, 0, str(self.active_dir.absolute()), curses.COLS)
        self.stdscr.hline(1, 0, curses.A_HORIZONTAL, curses.COLS)
        return 2

    def resize(self):
        """Handler for a KEY_RESIZE event."""
        curses.resize_term(*self.stdscr.getmaxyx())
        curses.curs_set(Cursor.HIDDEN)
        self.render()

    @property
    def active_item_index(self) -> int:
        """Index of the selected item in panes[1]."""
        return self._active_item_index

    @active_item_index.setter
    def active_item_index(self, value: int):
        if value < 0:
            self._active_item_index = 0
        elif value >= self._max_cursor_index:
            self._active_item_index = self._max_cursor_index
        else:
            self._active_item_index = value

        self.render()
