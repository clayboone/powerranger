import curses
import logging
from pathlib import Path
from typing import Optional
import win32api

import config
from files import Directory, Item
from singleton import SingletonMeta

_log = logging.getLogger(__name__)  # pylint: disable=invalid-name


def start_curses():
    _log.debug("Enabling curses")
    stdscr = curses.initscr()
    curses.cbreak()
    curses.noecho()
    stdscr.keypad(True)

    if curses.has_colors():
        curses.start_color()

    View(stdscr).render()


def stop_curses():
    _log.debug("Disabling curses")
    curses.echo()
    curses.nocbreak()
    curses.endwin()


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
        # curses.newwin for code completion.
        self.stdscr: curses.newwin = stdscr
        self.active_dir = Path(config.DEFAULT_STARTUP_DIR).resolve()
        self._active_item_index = 0
        self._active_top_index = 0
        self.active_item: Optional[Path] = None
        self._max_cursor_index = None

    def render(self):
        """Render the main window view."""
        panes = []

        # Header.
        header_offset = self._draw_header()
        border_offset = int(config.View.draw_boxes)
        height = curses.LINES - header_offset

        # Parent pane.
        parent_width = int(curses.COLS * config.View.parent_pane_width_percent)
        parent_start = 0
        panes.append(curses.newwin(height, parent_width, header_offset, parent_start))

        # Path.parent returns itself if it is the root, so index instead.
        try:
            active_dir_parent = Directory(self.active_dir.parents[0])
        except IndexError:
            drives = win32api.GetLogicalDriveStrings().split('\x00')[:-1]
            active_dir_parent = (Item(drive) for drive in drives)

        for index, item in enumerate(active_dir_parent):
            item.selected = item.name == self.active_dir.name

            item_text = item.name or str(item.path)
            panes[0].addnstr(index + border_offset, border_offset, item_text, parent_width, item.color)

        # Active pane.
        active_width = int(curses.COLS * config.View.active_pane_width_percent)
        active_start = parent_start + parent_width
        panes.append(curses.newwin(height, active_width, header_offset, active_start))

        visible_items = list(Directory(self.active_dir))[slice(
            self._active_top_index,
            self._active_top_index + (height - 2*border_offset),
        )]

        for index, item in enumerate(visible_items):
            if index == self.active_item_index:
                self.active_item = item.path
                item.selected = True

            self._max_cursor_index = index

            panes[1].addnstr(index + border_offset, border_offset, item.name, active_width, item.color)

        content_width = curses.COLS - (parent_width+active_width)
        content_start = active_start + active_width
        panes.append(curses.newwin(height, content_width, header_offset, content_start))

        self.stdscr.refresh()

        for pane in panes:
            if config.View.draw_boxes:
                pane.box()

            pane.refresh()

    def _draw_header(self) -> int:
        """Draw the View's header text and line.

        @return The combined vertical offset
        """
        foldername = str(self.active_dir.absolute())
        header_text = foldername + " " * (curses.COLS - len(foldername))

        self.stdscr.addnstr(0, 0, header_text, curses.COLS)
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
