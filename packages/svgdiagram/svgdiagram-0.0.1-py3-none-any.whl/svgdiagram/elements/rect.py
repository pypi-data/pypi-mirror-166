from .svg_element import SvgElement


class Rect(SvgElement):
    def __init__(self, x, y, width, height, rx=None, ry=None, attributes=None, children=None) -> None:
        attribs = attributes if attributes else {}
        attribs.update({
            "x": x,
            "y": y,
            "width": width,
            "height": height,
            "rx": rx,
            "ry": ry,
        })
        super().__init__('rect', attribs, children)

    @classmethod
    def midpoint_round_rect(cls, mid_x, mid_y, width, height, radius, attributes=None, children=None):
        return Rect(
            x=mid_x - width/2,
            y=mid_y - height/2,
            width=width,
            height=height,
            rx=radius,
            ry=radius,
            attributes=attributes,
            children=children,
        )
