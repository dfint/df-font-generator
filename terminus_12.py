from pathlib import Path

from df_font_generator.font_generator import CP1251_CHARMAP, FontGenerator

fg = FontGenerator()
fg.set_font(Path("./fonts/terminus.ttf"), 12)

for line in CP1251_CHARMAP:
    fg.draw_sequence(line)

# Saving the image to the file system.
fg.save(Path("./curses_640x300.png"))
