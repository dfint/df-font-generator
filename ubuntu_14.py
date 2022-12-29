from pathlib import Path

from df_font_generator.font_generator import CP1251_CHARMAP, FontGenerator

fg = FontGenerator()
fg.set_padding(0, -1)
fg.set_font(Path("./fonts/ubuntu_mono.ttf"), 14)

for line in CP1251_CHARMAP:
    fg.draw_sequence(line)

fg.set_padding(0, 0)
fg.set_font(Path("./Terminess (TTF) Nerd Font Complete Mono.ttf"), 14)
fg.patch_unknown_chars()

fg.set_position(14, 9)
fg.draw_char("₧")
fg.set_position(9, 10)
fg.draw_char("⌐")


fg.set_padding(0, -1)
fg.set_font(Path("./Ubuntu Mono Nerd Font Complete Mono Windows Compatible.ttf"), 14)
fg.set_position(15, 6)
fg.draw_char("o")
fg.set_position(14, 8)
fg.draw_char("Ä")
fg.set_position(15, 8)
fg.draw_char("Ă")
fg.set_position(9, 9)
fg.draw_char("O")


# Saving the image to the file system.
fg.save(Path("./curses_640x300.png"))
