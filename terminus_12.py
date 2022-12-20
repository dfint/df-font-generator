from pathlib import Path

from curses_generator import CursesGenerator, CP1251_CHARMAP


cg = CursesGenerator()
cg.set_font(Path("./Terminess (TTF) Nerd Font Complete Mono.ttf"), 12)

for line in CP1251_CHARMAP:
    cg.draw_sequence(line)

# Saving the image to the file system.
cg.save(Path("./curses_640x300.png"))
