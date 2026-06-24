import marimo

__generated_with = "0.18.0"
app = marimo.App()

with app.setup(hide_code=True):
    from pathlib import Path
    from PIL import Image
    import marimo as mo

    from df_font_generator.font_generator import FontGenerator


@app.function
def get_font() -> Image.Image:
    fg = FontGenerator()
    fg.set_font(Path("./fonts/terminus_bold.ttf"), 14)
    fg.set_charset(encoding="cp866")

    # clear all canvas mode
    fg.clear_canvas()
    fg.set_padding(0, -1)
    fg.draw_full_charset()

    fg.set_padding(0, 0)
    # Redraw characters, which are cut with padding (0, -1)
    fg.redraw_characters("§^~")

    # Redraw characters not used for Russian language
    fg.set_charset(encoding="cp437")
    fg.redraw_characters("≡√≥≤⌠⌡÷≈°")

    return fg.image


@app.cell
def create_font_image():
    image = get_font()
    return (image,)


@app.cell(hide_code=True)
def show_image_preview(image):
    # Show resulting image (upscaled to see details)
    preview = None
    if mo.running_in_notebook():
        scale = 2
        width = image.width * scale
        height = image.height * scale
        preview = image.resize((width, height), Image.Resampling.NEAREST)

    preview  # type: ignore
    return


@app.cell(hide_code=True)
def create_run_button():
    button = mo.ui.run_button(label="Write font file")
    button  # type: ignore
    return (button,)


@app.cell(hide_code=True)
def write_font_file(button, image):
    if button.value:
        file = "cp866r.png"
        image.save(file)
        print(f"File {file} written")
    return


if __name__ == "__main__":
    app.run()
