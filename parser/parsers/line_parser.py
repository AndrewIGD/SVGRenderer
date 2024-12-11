from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.line_drawer import Line
from parser.parsers.parser_base import Parser
from parser.utils import compare_tag


class LineParser(Parser):
    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "line"):
            return None

        if "x1" in element.keys():
            x1 = float(element.get("x1"))
        else: return None

        if "x2" in element.keys():
            x2 = float(element.get("x2"))
        else:
            return None

        if "y1" in element.keys():
            y1 = float(element.get("y1"))
        else: return None

        if "y2" in element.keys():
            y2 = float(element.get("y2"))
        else: return None

        return Line(x1, y1, x2, y2, config)