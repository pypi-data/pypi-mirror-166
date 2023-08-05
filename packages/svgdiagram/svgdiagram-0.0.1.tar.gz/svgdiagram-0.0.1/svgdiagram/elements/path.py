from .svg_element import SvgElement


class Path(SvgElement):
    def __init__(self, points, attributes=None) -> None:

        d = f'M {points[0][0]} {points[0][1]}'

        for p in points[1:]:
            d += f' L {p[0]} {p[1]}'

        attributes = attributes if attributes else {}

        attributes['d'] = d

        super().__init__('path', attributes)
