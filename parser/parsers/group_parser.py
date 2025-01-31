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
        """
          Tries to parse an XML element into a Group element.

          Args:
              element (Element): XML node
              config (SVGConfig): Parsing settings

          Returns:
              SVG: The Group element, containing its children
              None: otherwise
           """

        if not compare_tag(element, "g"):
            return None

        self.group = Group(0, 0, 0, 0, config)
        self.parse_children(element, config)

        return self.group

    def parse_children(self, element: Element, config: SVGConfig):
        """
          Parses all the children of an XML node into valid SVG elements and stores them in the group.

          Args:
              element (Element): XML node
              config (SVGConfig): Parsing settings
           """

        iterator = element.iter()
        for child in iterator:
            if child is element:
                continue

            drawable = get_parsing_function()(child, config)
            if drawable is not None:
                self.group.add_child(drawable)