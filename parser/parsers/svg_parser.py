from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.svg_drawer import SVG
from parser.parsers.group_parser import GroupParser
from parser.utils import compare_tag


class SVGParser(GroupParser):
    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "svg"):
            return None

        if "viewBox" not in element.keys():
            raise ValueError("Element does not have 'viewBox'")

        view_box = element.get("viewBox")
        x, y, width, height = view_box.split(" ")

        self.group = SVG(float(x), float(y), float(width), float(height), config)
        self.parse_children(element, config)

        print(len(self.group.children))
        for child in self.group.children:
            print(child)

        return self.group