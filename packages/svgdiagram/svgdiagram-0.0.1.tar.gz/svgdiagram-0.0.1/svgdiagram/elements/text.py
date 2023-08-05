from .svg_element import SvgElement


class Text(SvgElement):
    def __init__(self, x, y, text, attributes=None, children=None) -> None:
        attribs = attributes if attributes else {}
        attribs.update({
            "x": x,
            "y": y,
        })
        super().__init__('text', attribs, children=[text])
