from PIL import Image, ImageDraw, ImageFont
from typing import Optional, TypeAlias
from enum import Enum
from pathlib import Path


CP1251_CHARMAP = [
    " ☺☻♥♦♣♠●◘○◙♂♀♪♫☼",
    "▶◀↕‼¶§▬↨↑↓→←∟↔▲▼",
    " !\"#$%&'()*+,-./",
    "0123456789:;<=>?",
    "@ABCDEFGHIJKLMNO",
    "PQRSTUVWXYZ[\\]^_",
    "`abcdefghijklmno",
    "pqrstuvwxyz{|}~⌂",
    "ÇüéâäàăçêëèïîìÄĂ",
    "ÉæÆôöòûùÿOU¢£¥₧ƒ",
    "áЎўúñҐªºË⌐Є½¼¡«»",
    "░▒Iiґ╡╢╖ë╣║╗╝╜Ïï",
    "АБВГДЕЖЗИЙКЛМНОП",
    "РСТУФХЦЧШЩЪЫЬЭЮЯ",
    "абвгдежзийклмноп",
    "рстуфхцчшщъыьэюя",
]

CP437_CHARMAP = [
    " ☺☻♥♦♣♠●◘○◙♂♀♪♫☼",
    "▶◀↕‼¶§▬↨↑↓→←∟↔▲▼",
    " !\"#$%&'()*+,-./",
    "0123456789:;<=>?",
    "@ABCDEFGHIJKLMNO",
    "PQRSTUVWXYZ[\\]^_",
    "`abcdefghijklmno",
    "pqrstuvwxyz{|}~⌂",
    "ÇüéâäàăçêëèïîìÄĂ",
    "ÉæÆôöòûùÿOU¢£¥₧ƒ",
    "áíóúñÑªº¿⌐¬½¼¡«»",
    "░▒▓│┤╡╢╖╕╣║╗╝╜╛┐",
    "└┴┬├─┼╞╟╚╔╩╦╠═╬╧",
    "╨╤╥╙╘╒╓╫╪┘┌█▄▌▐▀",
    "αßΓπΣσµτΦΘΩδ∞φε∩",
    "≡±≥≤⌠⌡÷≈°∙·√ⁿ²■ ",
]


Size: TypeAlias = tuple[int, int]
Position = tuple[int, int]
Coordinate: TypeAlias = tuple[float, float]
Color: TypeAlias = tuple[int, int, int]


class Axis(Enum):
    X = 1
    Y = 2
    XY = 3


class CursesGenerator:
    canvas: Size
    box_size: Size
    font_color: Color
    background_color: Color
    image: Image.Image
    draw: ImageDraw.ImageDraw
    font: ImageFont.FreeTypeFont
    position: Position
    padding: Coordinate

    def __init__(
        self,
        source: Optional[Path] = None,
        canvas: Size = (128, 192),
        box_size: Size = (8, 12),
        font_color: Color = (255, 255, 255),
        background_color: Color = (255, 0, 255),
    ) -> None:
        self.font_color = font_color
        self.background_color = background_color
        self.box_size = box_size
        self.position = (0, 0)
        self.padding = (0, 0)
        if source:
            self.image = Image.open(source)
            self.canvas = self.image.size
        else:
            self.canvas = canvas
            self.image = Image.new("P", self.canvas, self.background_color)
        self.draw = ImageDraw.Draw(self.image)

    def save(self, path: Path) -> None:
        self.image.save(path)

    def set_font(self, ttf_path: Path, size: int) -> None:
        self.font = ImageFont.truetype(font=str(ttf_path.resolve()), size=size)

    def set_padding(self, padding: Coordinate) -> None:
        self.padding = padding

    def __coordx(self, value: int) -> float:
        return value * self.box_size[0]

    def __coordy(self, value: int) -> float:
        return value * self.box_size[1]

    def __coords(self, position: Position) -> Coordinate:
        return (position[0] * self.box_size[0], position[1] * self.box_size[1])

    def __increment_position(self, axis: Axis = Axis.XY) -> None:
        if axis == Axis.X:
            self.position = (self.position[0] + 1, self.position[1])
        elif axis == Axis.Y:
            self.position = (self.position[0], self.position[1] + 1)
        elif axis == Axis.XY:
            self.position = (self.position[0] + 1, self.position[1] + 1)

    def next_position(self) -> None:
        self.__increment_position(Axis.X)
        if self.__coordx(self.position[0]) >= self.canvas[0]:
            self.position = (0, self.position[1] + 1)

    def set_position(self, position: Position) -> None:
        coords = self.__coords(position)
        if coords[0] >= self.canvas[0] or coords[1] >= self.canvas[1]:
            raise Exception("Position points out of canvas")
        self.position = position

    def get_charset(
        self, encoding: str = "cp1251", rng: tuple[int, int] = (128, 256)
    ) -> str:
        missing_chars: list[int] = list()
        charset_bytes = bytes(range(*rng))
        try:
            charset_bytes.decode(encoding, errors="strict")
        except ValueError as e:
            missing_chars.append(e.args[2])
        return self.patch_missing_chars(
            charset_bytes.decode(encoding, errors="replace"), missing_chars
        )

    def patch_missing_chars(self, charset: str, missing: list[int]) -> str:
        sample = list("".join(CP437_CHARMAP))
        charset_list = list(charset)
        for item in missing:
            charset_list[item] = sample[item]
        return "".join(charset_list)

    def clear_canvas(self) -> None:
        self.draw.rectangle(
            xy=(0, 0, *self.canvas),
            fill=self.background_color,
            width=0,
            outline=None,
        )

    def draw_char(self, char: str, fill_box: bool = True) -> None:
        assert isinstance(
            self.font, ImageFont.FreeTypeFont
        ), "Set font before printing chars"
        if self.__coordy(self.position[1]) >= self.canvas[1]:
            raise Exception("To many raws for this canvas size")
        if len(char) > 1:
            raise Exception("Pass single char instead of string")
        coords = self.__coords(self.position)
        if fill_box:
            self.draw.rectangle(
                xy=(
                    coords,
                    (coords[0] + self.box_size[0], coords[1] + self.box_size[1]),
                ),
                fill=self.background_color,
                width=0,
                outline=None,
            )
        self.draw.multiline_text(
            xy=(
                coords[0] + self.box_size[0] / 2 + self.padding[0],
                coords[1] + self.box_size[1] / 2 + self.padding[1],
            ),
            text=char,
            font=self.font,
            fill=self.font_color,
            align="center",
            anchor="mm",
        )

    def draw_sequence(self, text: str, fill_box: bool = True) -> None:
        for char in list(text):
            self.draw_char(char, fill_box)
            self.next_position()
