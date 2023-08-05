from dataclasses import dataclass
from svgdiagram.elements.rect import Rect
from svgdiagram.elements.text import Text
from svgdiagram.elements.group import Group


@dataclass
class TextLine:
    text: str
    font_size: float = 16.0
    font_family: str = "arial"
    font_weight: str = 'normal'


class MultiLineRect(Group):
    def __init__(self, x, y, width, padding=5, line_gap=2, radius=None, text_lines=None, attributes=None):
        height = padding
        children = []

        for line in text_lines:

            children.append(Text(x + width / 2, y+height + line.font_size/2, line.text, attributes={
                "text-anchor": "middle",
                "alignment-baseline": "central",
                "font-family": line.font_family,
                "font-size": line.font_size,
                "font-weight": line.font_weight
            }))
            height += line.font_size + line_gap

        height += padding

        super().__init__(children=[Rect(x, y, width, height, radius, radius, attributes)] + children)
