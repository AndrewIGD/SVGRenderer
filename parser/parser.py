import string
import xml.etree.ElementTree as ET

from drawer.drawer import SVGConfig
from parser.parsers.ellipse_parser import EllipseParser

from parser.parsers.group_parser import GroupParser
from parser.parsers.line_parser import LineParser
from parser.parsers.path_parser import PathParser
from parser.parsers.polyline_parser import PolylineParser
from parser.parsers.rectangle_parser import RectParser
from parser.parsers.svg_parser import SVGParser
from parser.utils import set_parsing_function

element_parsers = [
        SVGParser(), GroupParser(), RectParser(), EllipseParser(), LineParser(), PathParser(), PolylineParser()
    ]

def try_parse(element: ET.Element, config: SVGConfig):
    """
    Tries parsing an XML element into an SVG element from a list of pre-defined parsers shape parsers.

    Args:
        element (ET.Element): XML node
        config (SVGConfig): Parsing settings

    Returns:
        Drawable: valid SVG element
        None: otherwise
    """

    for parser in element_parsers:
        drawable = parser.try_parse(element, config)
        if drawable is not None:
            return drawable

    return None

def parse_svg(contents: string, svg_config: SVGConfig):
    """
    Parses svg contents to a valid SVG tree.

    Args:
        contents (str): SVG file contents
        svg_config (SVGConfig): Parsing settings

    Returns:
        SVG: The root node of the SVG tree

    Raises:
        Exception: If parsing fails
    """

    set_parsing_function(try_parse)

    tree = ET.parse(contents)
    svg = try_parse(tree.getroot(), svg_config)
    if svg is None:
        raise Exception("Could not parse SVG")

    return svg