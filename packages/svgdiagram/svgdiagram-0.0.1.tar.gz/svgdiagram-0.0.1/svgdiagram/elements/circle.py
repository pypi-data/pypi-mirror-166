from .svg_element import SvgElement


class Circle(SvgElement):
    def __init__(self, cx, cy, r, attributes) -> None:
        attributes['cx'] = cx
        attributes['cy'] = cy
        attributes['r'] = r
        super().__init__('circle', attributes)
