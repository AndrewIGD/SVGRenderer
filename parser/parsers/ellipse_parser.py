from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.ellipse_drawer import Ellipse
from parser.parsers.parser_base import Parser
from parser.utils import compare_tag


class EllipseParser(Parser):
    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "circle") and not compare_tag(element, "ellipse"):
            return None

        if "cx" in element.keys():
            cx = float(element.get("cx"))
        else: cx = 0

        if "cy" in element.keys():
            cy = float(element.get("cy"))
        else: cy = 0

        if "r" in element.keys():
            rx = ry = float(element.get("r"))
        else:
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

        return Ellipse(cx, cy, rx, ry, config)