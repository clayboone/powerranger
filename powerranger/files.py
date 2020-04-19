import curses
import itertools
from pathlib import Path
from typing import Optional, Union

from powerranger import config
from powerranger.colors import Colors


class Item:
    """An item inside of a Directory."""
    def __init__(self, path: Union[Path, str]):
        self._path = Path(path)
        self._selected = False

    @property
    def name(self) -> str:
        """The name of the item, not including parents."""
        return self._path.name

    @property
    def color(self) -> curses.color_pair:
        """An initialized ncurses color pair associated with the type of file
        for this Item.
        """
        if self.selected:
            return Colors.black_on_white()

        if self._path.is_dir():
            return Colors.blue_on_black()

        return Colors.default()

    @property
    def selected(self) -> Optional[bool]:
        """Return whether this item should appear as selected"""
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value


class Directory:
    """A list of items inside of a directory."""
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)

    def __iter__(self):
        items = self.path.iterdir()

        if config.SORT_FOLDERS_ON_TOP:
            items1, items2 = itertools.tee(items)
            items = itertools.chain(
                (item for item in items1 if item.is_dir()),
                (item for item in items2 if not item.is_dir()),
            )

        for item in items:
            yield Item(item)
