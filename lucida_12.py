from pathlib import Path

from curses_generator import CursesGenerator

cg = CursesGenerator()
cg.set_font(Path("./lucon.ttf"), 12)

# Use generated charset sequence
charset = cg.get_charset("cp1251")
cg.draw_sequence(charset)

# Lucida Patch missing glyphs
cg.set_font(Path("./Terminess (TTF) Nerd Font Complete Mono.ttf"), 12)
cg.patch_unknown_chars()

# Saving the image to the file system.
cg.save(Path("./curses_640x300.png"))
