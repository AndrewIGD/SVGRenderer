from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.ellipse_drawer import Ellipse
from drawer.drawers.polyline_drawer import Polyline
from parser.shape_parser import ShapeParser
from parser.utils import compare_tag


class PolylineParser(ShapeParser):
    def try_parse(self, element: Element, config: SVGConfig):
        """
          Tries to parse an XML element into a polyline element.

          Args:
              element (Element): XML node
              config (SVGConfig): Parsing settings

          Returns:
              SVG: The Polyline element, containing the points that define the polyline, along with styling
              None: otherwise
           """

        if not compare_tag(element, "polyline"):
            return None

        if not "points" in element.keys():
            return None

        self.outline = None

        self.parse_shape_elements(element)

        points = element.get("points").split(" ")

        parsed_points = []
        for point in points:
            coords = point.split(",")
            if len(coords) != 2:
                continue

            parsed_points.append(coords)

        return Polyline(parsed_points, config, self.fill, self.outline, self.outline_width)