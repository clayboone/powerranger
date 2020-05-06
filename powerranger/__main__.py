from cursescontext import CursesContext
from powerranger import powerranger

with CursesContext().curses_screen() as stdscr:
    powerranger.main(stdscr)
