import curses
import itertools
import os
from pathlib import Path
import stat
from typing import Optional, Union

import config
from colors import Colors


class Item:
    """An item inside of a Directory."""
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)
        self._selected = False

    @property
    def name(self) -> str:
        """The name of the item, not including parents."""
        return self.path.name

    @property
    def color(self) -> curses.color_pair:
        """An initialized curses color pair associated with the type of file
        for this Item.
        """
        if self.selected:
            return Colors.black_on_white()

        if self.path.is_dir():
            return Colors.blue_on_black()

        return Colors.default()

    @property
    def selected(self) -> Optional[bool]:
        """Return whether this item should appear as selected"""
        return self._selected

    @selected.setter
    def selected(self, value: bool):
        self._selected = value

    def is_hidden(self) -> bool:
        """Return whether or not the file should be hidden."""
        return self._has_hidden_attribute() or self.path.name.startswith(".")

    def _has_hidden_attribute(self) -> bool:
        try:
            return bool(os.stat(self.path.resolve()).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        except PermissionError:
            return True


class Directory:
    """A list of items inside of a directory."""
    def __init__(self, path: Union[Path, str]):
        self.path = Path(path)

    def __iter__(self):
        elements = self.path.iterdir()

        if config.SORT_FOLDERS_ON_TOP:
            element1, element2 = itertools.tee(elements)
            elements = itertools.chain(
                (item for item in element1 if item.is_dir()),
                (item for item in element2 if not item.is_dir()),
            )

        for element in elements:
            item = Item(element)

            if item.is_hidden() and not config.SHOW_HIDDEN_FILES:
                continue

            yield Item(element)
