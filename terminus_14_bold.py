from pathlib import Path

from curses_generator import CursesGenerator, CP1251_CHARMAP


cg = CursesGenerator(source=Path("./original.png"))
cg.set_font(
    Path("./Terminess (TTF) Bold Nerd Font Complete Mono Windows Compatible.ttf"), 14
)

# clear all canvas mode
cg.clear_canvas()
cg.set_padding((0, -1))

for line in CP1251_CHARMAP:
    cg.draw_sequence(line, False)

"""
Patch needed, cause some chars out of they boxes
"""
# Teminus 14 patch
cg.set_position((0, 5))
cg.draw_char(" ")
cg.draw_char("P", False)
cg.set_position((1, 5))
cg.draw_char("Q", False)
cg.set_position((1, 6))
cg.draw_char("a", False)

cg.set_position((14, 6))
cg.draw_char(" ")
cg.draw_char("n", False)
cg.set_position((15, 6))
cg.draw_char("o", False)

cg.set_position((14, 4))
cg.draw_char(" ")
cg.draw_char("N", False)
cg.set_position((15, 4))
cg.draw_char("O", False)


cg.set_padding((0, 1))
cg.set_position((0, 6))
cg.draw_char("`", False)


cg.set_position((15, 7))
cg.draw_char(" ")
cg.set_position((14, 7))
cg.draw_char("~")
cg.set_padding((0, -1))
cg.set_position((15, 7))
cg.draw_char("⌂", False)

cg.set_padding((0, 0))
cg.set_position((14, 5))
cg.draw_char("^")


# Saving the image to the file system.
cg.save(Path("./curses_640x300.png"))
