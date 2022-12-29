from pathlib import Path

from df_font_generator.font_generator import CP1251_CHARMAP, FontGenerator

# Load original one in this scenario
fg = FontGenerator(source=Path("./original.png"))
fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)

# clear all canvas mode
fg.clear_canvas()
fg.set_padding(0, -1)

for line in CP1251_CHARMAP:
    fg.draw_sequence(line, False)

"""
Patch needed, cause some chars out of they boxes
"""
# Terminus 14 patch
fg.set_position(0, 5)
fg.draw_char(" ")
fg.draw_char("P", False)
fg.set_position(1, 5)
fg.draw_char("Q", False)
fg.set_position(1, 6)
fg.draw_char("a", False)

fg.set_position(14, 6)
fg.draw_char(" ")
fg.draw_char("n", False)
fg.set_position(15, 6)
fg.draw_char("o", False)

fg.set_position(14, 4)
fg.draw_char(" ")
fg.draw_char("N", False)
fg.set_position(15, 4)
fg.draw_char("O", False)


fg.set_padding(0, 1)
fg.set_position(0, 6)
fg.draw_char("`", False)


fg.set_position(15, 7)
fg.draw_char(" ")
fg.set_position(14, 7)
fg.draw_char("~")
fg.set_padding(0, -1)
fg.set_position(15, 7)
fg.draw_char("⌂", False)

fg.set_padding(0, 0)
fg.set_position(14, 5)
fg.draw_char("^")

fg.draw_point(35, 155)

# Saving the image to the file system.
fg.save(Path("./curses_640x300.png"))
