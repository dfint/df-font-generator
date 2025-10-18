from pathlib import Path

from df_font_generator.font_generator import FontGenerator

fg = FontGenerator()
fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)

fg.set_charset(encoding="cp852")

# clear all canvas mode
fg.clear_canvas()
fg.set_padding(0, -1)
fg.draw_sequence(fg.get_charset(encoding="cp852"))

fg.set_padding(0, 0)
fg.set_position(0, 15)
fg.draw_char("≡")
fg.set_position(5, 1)
fg.draw_char("§")
fg.set_position(5, 15)
fg.draw_char("§")
fg.set_position(14, 5)
fg.draw_char("^")
fg.set_position(14, 7)
fg.draw_char("~")


fg.set_padding(0, 1)
fg.set_position(0, 6)
fg.draw_char("`")

chars = [
    0x8A,
    0x8D,
    0x8E,
    0x8F,
    0x90,
    0x91,
    0x95,
    0x96,
    0x97,
    0x99,
    0x9A,
    0x9B,
    0xA6,
    0xAC,
    0xB5,
    0xB6,
    0xB7,
    0xBD,
    0xC6,
    0xD2,
    0xD3,
    0xD5,
    0xD6,
    0xD7,
    0xDE,
    0xE0,
    0xE2,
    0xE3,
    0xE6,
    0xE8,
    0xE9,
    0xEB,
    0xED,
    0xF1,
    0xF3,
    0xF4,
    0xF8,
    0xF9,
    0xFA,
    0xFC,
]

for char in chars:
    fg.draw_from_charset(char)


# Saving the image to the file system.
fg.save(Path("./cp852.png"))
