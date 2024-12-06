from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.rect_drawer import Rectangle

from parser.parsers.parser_base import Parser
from parser.utils import compare_tag


class RectParser(Parser):
    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "rect"):
            return None

        if ("width" not in element.keys() or
                "height" not in element.keys() or
                "x" not in element.keys() or
                "y" not in element.keys()):
            raise ValueError("Invalid 'rect' element")

        width = float(element.get("width"))
        height = float(element.get("height"))
        x = float(element.get("x"))
        y = float(element.get("y"))

        if "rx" in element.keys():
            rx = float(element.get("rx"))
        else: rx = None

        if "ry" in element.keys():
            ry = float(element.get("ry"))
        else: ry = None

        if rx is None and ry is not None:
            rx = ry
        elif rx is not None and ry is None:
            ry = rx

        if rx > width / 2:
            rx = width / 2

        if ry > height / 2:
            ry = height / 2

        return Rectangle(x, y, width, height, rx, ry, config)