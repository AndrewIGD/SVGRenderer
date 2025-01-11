from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.ellipse_drawer import Ellipse
from parser.shape_parser import ShapeParser
from parser.utils import compare_tag


class EllipseParser(ShapeParser):
    def try_parse(self, element: Element, config: SVGConfig):
        """
          Tries to parse an XML element into an ellipse element. Circles are considered ellipses with equal rx and ry values.

          Args:
              element (Element): XML node
              config (SVGConfig): Parsing settings

          Returns:
              SVG: The Ellipse element, containing the center position, radii and styling
              None: otherwise
           """

        if not compare_tag(element, "circle") and not compare_tag(element, "ellipse"):
            return None

        self.parse_shape_elements(element)

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

        return Ellipse(cx, cy, rx, ry, config, self.fill, self.outline, self.outline_width)