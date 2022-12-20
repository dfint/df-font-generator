from pathlib import Path

from curses_generator import CursesGenerator, CP1251_CHARMAP


cg = CursesGenerator()
cg.set_font(Path("./lucon.ttf"), 12)

for line in CP1251_CHARMAP:
    cg.draw_sequence(line)

"""
Patch needed, cause some glyphs missing
"""
# Lucida Patch missing glyphs
cg.set_font(Path("./Terminess (TTF) Nerd Font Complete Mono.ttf"), 12)
cg.set_position((0, 1))
cg.draw_sequence("▶◀")
cg.set_position((10, 10))
cg.draw_sequence("Ɛ")

# Saving the image to the file system.
cg.save(Path("./curses_640x300.png"))
