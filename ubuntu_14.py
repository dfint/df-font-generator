from pathlib import Path

from curses_generator import CP1251_CHARMAP, CursesGenerator

cg = CursesGenerator()
cg.set_padding(0, -1)
cg.set_font(Path("./Ubuntu Mono Nerd Font Complete Mono Windows Compatible.ttf"), 14)

for line in CP1251_CHARMAP:
    cg.draw_sequence(line)

cg.set_padding(0, 0)
cg.set_font(Path("./Terminess (TTF) Nerd Font Complete Mono.ttf"), 14)
cg.patch_unknown_chars()

cg.set_position(14, 9)
cg.draw_char("₧")
cg.set_position(9, 10)
cg.draw_char("⌐")


cg.set_padding(0, -1)
cg.set_font(Path("./Ubuntu Mono Nerd Font Complete Mono Windows Compatible.ttf"), 14)
cg.set_position(15, 6)
cg.draw_char("o")
cg.set_position(14, 8)
cg.draw_char("Ä")
cg.set_position(15, 8)
cg.draw_char("Ă")
cg.set_position(9, 9)
cg.draw_char("O")


# Saving the image to the file system.
cg.save(Path("./curses_640x300.png"))
