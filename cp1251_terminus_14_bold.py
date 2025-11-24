from pathlib import Path

from df_font_generator.font_generator import FontGenerator

fg = FontGenerator()
fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)
fg.set_charset(encoding="cp1251")

# clear all canvas mode
fg.clear_canvas()
fg.set_padding(0, -1)
fg.draw_full_charset()

# Patch needed, cause some chars out of they boxes
# Terminus 14 patch
fg.set_position(0, 5)
fg.draw_char(" ")
fg.draw_char("P", fill_box=False)
fg.set_position(1, 5)
fg.draw_char("Q", fill_box=False)
fg.set_position(1, 6)
fg.draw_char("a", fill_box=False)

fg.set_position(14, 6)
fg.draw_char(" ")
fg.draw_char("n", fill_box=False)
fg.set_position(15, 6)
fg.draw_char("o", fill_box=False)

fg.set_position(14, 4)
fg.draw_char(" ")
fg.draw_char("N", fill_box=False)
fg.set_position(15, 4)
fg.draw_char("O", fill_box=False)


fg.set_padding(0, 1)
fg.set_position(0, 6)
fg.draw_char("`", fill_box=False)


fg.set_position(15, 7)
fg.draw_char(" ")
fg.set_position(14, 7)
fg.draw_char("~")
fg.set_padding(0, -1)
fg.set_position(15, 7)
fg.draw_char("⌂", fill_box=False)

fg.set_padding(0, 0)
fg.set_position(14, 5)
fg.draw_char("^")

fg.draw_point(35, 155)

# Saving the image to the file system.
fg.save(Path("./cp1251.png"))
