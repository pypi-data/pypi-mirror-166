from yattag import Doc, indent


class SvgElement:
    def __init__(self, tag_name, attributes=None, children=None) -> None:
        self.tag_name = tag_name
        self.attributes = attributes if attributes else {}

        if not isinstance(children, list) and children:
            children = [children]

        self.children = children if children else []

    def render(self, debug=False, indent_count=None):
        doc, tag, text = Doc().tagtext()

        self._render(doc, tag, text, debug)

        svg_text = doc.getvalue()
        if indent_count:
            svg_text = indent(svg_text, ' '*indent_count)
        return svg_text

    def _render_local(self, doc, tag, text, debug):
        pass

    def _render(self, doc, tag, text, debug):
        kv_attribs = [(k, v) for k, v in self.attributes.items()]

        with tag(self.tag_name, *kv_attribs):
            self._render_local(doc, tag, text, debug)
            for child in self.children:
                if isinstance(child, str):
                    text(child)
                else:
                    child._render(doc, tag, text, debug)

    def add_child(self, child):
        self.children.append(child)
