from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig, Drawable


class Parser:
    def __init__(self):
        pass

    def try_parse(self, element: Element, config: SVGConfig) -> Drawable:
        """
        Tries to parse an XML element into this parser's shape type.

        Args:
            element (Element): XML node
            config (SVGConfig): Parsing settings

        Returns:
            Drawable: This parser's valid shape object
            None: otherwise
        """
        pass