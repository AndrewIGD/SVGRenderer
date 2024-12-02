from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.group_drawer import Group
from parser.parsers.parser_base import Parser

from parser.utils import get_parsing_function, compare_tag


class GroupParser(Parser):
    def __init__(self):
        super().__init__()
        self.group = None

    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "g"):
            return None

        self.group = Group(0, 0, 0, 0, config)
        self.parse_children(element, config)

        return self.group

    def parse_children(self, element: Element, config: SVGConfig):
        iterator = element.iter()
        for child in iterator:
            if child is element:
                continue

            drawable = get_parsing_function()(child, config)
            if drawable is not None:
                self.group.add_child(drawable)