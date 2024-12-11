import string
import xml.etree.ElementTree as ET

from drawer.drawer import SVGConfig
from parser.parsers.ellipse_parser import EllipseParser

from parser.parsers.group_parser import GroupParser
from parser.parsers.line_parser import LineParser
from parser.parsers.rectangle_parser import RectParser
from parser.parsers.svg_parser import SVGParser
from parser.utils import set_parsing_function

element_parsers = [
        SVGParser(), GroupParser(), RectParser(), EllipseParser(), LineParser()
    ]

def try_parse(element: ET.Element, config: SVGConfig):
    for parser in element_parsers:
        drawable = parser.try_parse(element, config)
        if drawable is not None:
            return drawable

    return None

def parse_svg(contents: string, svg_config: SVGConfig):
    set_parsing_function(try_parse)

    tree = ET.parse(contents)
    svg = try_parse(tree.getroot(), svg_config)
    if svg is None:
        raise Exception("Could not parse SVG")

    return svg