from pathlib import Path

from df_font_generator.font_generator import FontGenerator

fg = FontGenerator()
fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)
fg.set_charset(encoding="cp852")

# clear all canvas mode
fg.clear_canvas()
fg.set_padding(0, -1)
fg.draw_full_charset()

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

fg.redraw_characters("ŐŹÄĆÉĹĽľŚÖÜŤŽČÁÂĚŻĂĎËŇÍÎŮÓÔŃŠŔÚŰÝ˝ˇ˘°¨˙Ř")

# Saving the image to the file system.
fg.save(Path("./cp852.png"))
