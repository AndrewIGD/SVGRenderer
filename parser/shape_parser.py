import math
from xml.etree.ElementTree import Element

from parser.parsers.parser_base import Parser


class ShapeParser(Parser):
    def __init__(self):
        """
           Initializes common shape default styling.
        """

        super().__init__()
        self.fill = "#000000"
        self.outline = "#000000"
        self.outline_width = 1

    def parse_shape_elements(self, element: Element):
        """
        Parses common attributes applicable to most SVG elements (i.e. fill, stroke, stroke-width, style)

        Args:
            element (Element): XML node
        """

        if "fill" in element.keys():
            self.fill = element.get("fill")

        if "stroke" in element.keys():
            self.outline = element.get("stroke")

        if "stroke-width" in element.keys():
            self.outline_width = math.floor(float(element.get("stroke-width")))

        if "style" in element.keys():
            style = element.get("style")
            style_params = style.split(";")

            for param in style_params:
                pair = param.strip(" ").split(":")

                if len(pair) != 2:
                    continue

                key, value = pair

                if key == "fill":
                    self.fill = value
                elif key == "stroke":
                    self.outline = value
                elif key == "stroke-width":
                    self.outline_width = float(value)

        if self.fill is None or self.fill.lower() == "none":
            self.fill = None

        if self.outline is None or self.outline.lower() == "none":
            self.outline = None

        self.outline = "#000000"