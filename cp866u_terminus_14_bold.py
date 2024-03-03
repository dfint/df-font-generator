from pathlib import Path

from df_font_generator.font_generator import FontGenerator

fg = FontGenerator()
fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)


# clear all canvas mode
fg.clear_canvas()
fg.set_padding(0, -1)
fg.draw_sequence(fg.get_charset(encoding="cp866u"))

fg.set_padding(0, 0)
fg.set_position(0, 15)
fg.draw_char("≡")

# Saving the image to the file system.
fg.save(Path("./curses_640x300.png"))
