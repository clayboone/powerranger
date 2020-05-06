import cursescontext
from powerranger import powerranger

with cursescontext.start() as stdscr:
    powerranger.main(stdscr)
