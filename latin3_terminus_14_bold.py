import marimo

__generated_with = "0.18.0"
app = marimo.App()

with app.setup:
    from pathlib import Path
    from PIL import Image
    import marimo as mo

    from df_font_generator.font_generator import FontGenerator


@app.function
def get_latin3_font() -> Image.Image:
    fg = FontGenerator()
    fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)
    fg.set_charset(encoding="latin3")

    # clear all canvas mode
    fg.clear_canvas()
    fg.set_padding(0, -1)
    fg.draw_full_charset()

    # Patch needed, cause some chars out of they boxes
    # Terminus 14 patch
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

    fg.redraw_characters("°²³ĥÀÁÂÄĊĈÈÉÊËÌÍÎÏÑÒÓÔĠÖĜÙÚÛÜŬŜ")
    return fg.image


@app.cell
def _():
    image = get_latin3_font()
    return (image,)


@app.cell
def _(image):
    file = "latin3.png"
    image.save(file)
    print(f"File {file} written")
    return


@app.cell
def _(image):
    # Show resulting image (scaled x2 to see details)
    img = None
    if mo.running_in_notebook():
        scale = 2
        width = image.width * scale
        height = image.height * scale
        img = image.resize((width, height), Image.Resampling.NEAREST)

    img
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
