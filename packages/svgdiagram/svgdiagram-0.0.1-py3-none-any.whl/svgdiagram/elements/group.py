from .svg_element import SvgElement


class Group(SvgElement):
    def __init__(self, children=None) -> None:
        super().__init__('g', children=children)
