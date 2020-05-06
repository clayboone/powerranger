"""Configuration for powerranger."""
import os

DEFAULT_STARTUP_DIR = os.curdir
SORT_FOLDERS_ON_TOP = True
SHOW_HIDDEN_FILES = False
EDITOR = "notepad"


class View:
    """Generic settings for view.View."""
    draw_boxes = True
    parent_pane_width_percent = 0.15
    active_pane_width_percent = 0.45
