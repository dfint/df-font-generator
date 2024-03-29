import math
from enum import Enum
from pathlib import Path
from typing import NamedTuple, Optional

from alternative_encodings import cp859, cp866i, viscii
from PIL import Image, ImageDraw, ImageFont

cp859.register()
cp866i.register()
viscii.register()

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
    "áЎўúñҐªºË⌐Є½¼¡«Ï",
    "░▒Iiґ╡╢╖ë╣є╗╝╜╛ï",
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


class Size(NamedTuple):
    width: int
    height: int


class Position(NamedTuple):
    x: int
    y: int


class Coordinate(NamedTuple):
    x: float
    y: float


class Color(NamedTuple):
    r: int
    b: int
    g: int


class Axis(Enum):
    X = 1
    Y = 2
    XY = 3


class FontGenerator:
    canvas: Size
    box_size: Size
    font_color: Color
    background_color: Color
    image: Image.Image
    draw: ImageDraw.ImageDraw
    font: ImageFont.FreeTypeFont
    position: Position
    padding: Coordinate
    charset: str

    def __init__(
        self,
        source: Optional[Path] = None,
        canvas: Size = Size(128, 192),
        box_size: Size = Size(8, 12),
        font_color: Color = Color(255, 255, 255),
        background_color: Color = Color(255, 0, 255),
    ) -> None:
        self.font_color = font_color
        self.background_color = background_color
        self.box_size = box_size
        self.position = Position(0, 0)
        self.padding = Coordinate(0, 0)
        if source:
            self.image = Image.open(source)
            self.canvas = Size(*self.image.size)
        else:
            self.canvas = canvas
            self.image = Image.new("RGB", self.canvas, self.background_color)
        self.draw = ImageDraw.Draw(self.image)

    def save(self, path: Path) -> None:
        self.image.save(path)

    def set_font(self, ttf_path: Path, size: int) -> None:
        self.font = ImageFont.truetype(font=str(ttf_path.resolve()), size=size)

    def set_padding(self, x: float = 0, y: float = 0) -> None:
        self.padding = Coordinate(x, y)

    def __coords(self, position: Position) -> Coordinate:
        return Coordinate(
            position.x * self.box_size.width, position.y * self.box_size.height
        )

    def __increment_position(self, axis: Axis = Axis.XY) -> None:
        if axis == Axis.X:
            self.position = Position(self.position.x + 1, self.position.y)
        elif axis == Axis.Y:
            self.position = Position(self.position.x, self.position.y + 1)
        elif axis == Axis.XY:
            self.position = Position(self.position.x + 1, self.position.y + 1)

    def next_position(self) -> None:
        self.__increment_position(Axis.X)
        if self.__coords(self.position).x >= self.canvas.width:
            self.position = Position(0, self.position.y + 1)

    def set_position(self, x: int = 0, y: int = 0) -> None:
        coords = self.__coords(Position(x, y))
        if coords.x >= self.canvas.width or coords.y >= self.canvas.height:
            raise Exception("Position points out of canvas")
        self.position = Position(x, y)

    def get_charset(
        self, encoding: str = "cp1251", rng: tuple[int, int] = (0, 256)
    ) -> str:
        charset_bytes = bytes(range(*rng))
        charset = charset_bytes.decode(encoding, errors="replace")
        charset = self.patch_unprintable_chars(charset)
        return charset

    def set_charset(
        self, encoding: str = "cp1251", rng: tuple[int, int] = (0, 256)
    ) -> None:
        self.charset = self.get_charset(encoding)

    def patch_unprintable_chars(self, charset: str) -> str:
        charset_list = list(charset)
        for index, char in enumerate(charset):
            if repr(char).startswith("'\\x") or repr(char) in [
                "'\\t'",
                "'\\n'",
                "'\\r'",
                "'�'",
            ]:
                charset_list[index] = self.char_from_sample(index)
        return "".join(charset_list)

    def patch_unknown_chars(self) -> None:
        self.set_position(0, 0)
        self.draw_sequence(CP437_CHARMAP[0])
        self.draw_sequence(CP437_CHARMAP[1])
        self.set_position(15, 7)
        self.draw_sequence(CP437_CHARMAP[7][15])

    def char_from_sample(self, index: int) -> str:
        return list("".join(CP437_CHARMAP))[index]

    def clear_canvas(self) -> None:
        self.draw.rectangle(
            xy=(0, 0, self.canvas.width, self.canvas.height),
            fill=self.background_color,
            width=0,
            outline=None,
        )

    def draw_char_at_position(self, char: str, position: int) -> None:
        self.set_position(position % 16, math.floor(position / 16))
        self.draw_char(char)
        self.next_position()

    def draw_from_charset(self, position: int) -> None:
        if not self.charset:
            raise Exception("Set charset before drawing")
        self.draw_char_at_position(self.charset[position], position)

    def draw_char(self, char: str, fill_box: bool = True) -> None:
        assert isinstance(
            self.font, ImageFont.FreeTypeFont
        ), "Set font before printing chars"
        coords = self.__coords(self.position)
        if coords.x >= self.canvas.width or coords.y >= self.canvas.height:
            raise Exception("Position out of canvas")
        if len(char) > 1:
            raise Exception("Pass single char instead of string")
        box = Image.new("P", self.box_size, self.background_color)
        draw = ImageDraw.Draw(box)
        if fill_box:
            draw.rectangle(
                xy=(0, 0, self.box_size.width, self.box_size.height),
                fill=self.background_color,
                width=0,
                outline=None,
            )
        draw.multiline_text(
            xy=(
                self.box_size.width / 2 + self.padding.x,
                self.box_size.height / 2 + self.padding.y,
            ),
            text=char,
            font=self.font,
            fill=(255, 255, 255),
            align="center",
            anchor="mm",
        )
        self.image.paste(box, (math.floor(coords.x), math.floor(coords.y)))

    def draw_point(self, x: int, y: int) -> None:
        if x >= self.canvas.width or y >= self.canvas.height:
            raise Exception("Coordinates out of canvas")
        self.draw.point(xy=(x, y), fill=self.background_color)

    def draw_sequence(self, text: str, fill_box: bool = True) -> None:
        for char in list(text):
            self.draw_char(char, fill_box)
            self.next_position()
