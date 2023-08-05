from .svg_element import SvgElement


class Svg(SvgElement):
    def __init__(self) -> None:
        super().__init__('svg', attributes={
            "xmlns": "http://www.w3.org/2000/svg",
        })
