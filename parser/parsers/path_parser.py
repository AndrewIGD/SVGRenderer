from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.path_commands.cubic_curve import CubicCurve
from drawer.drawers.path_commands.line_to import LineTo
from drawer.drawers.path_commands.move_to import MoveTo
from drawer.drawers.path_commands.smooth_cubic import SmoothCubicCurve
from drawer.drawers.path_drawer import Path
from parser.parsers.parser_base import Parser
from parser.utils import compare_tag


class PathParser(Parser):
    def __init__(self):
        super().__init__()
        self.parameters = []
        self.index = 0
        self.commands = []
        self.relative = False

        self.previous_control = None

    def tokens_available(self):
        return self.index < len(self.parameters)

    def next_token(self):
        while self.tokens_available() and len(self.parameters[self.index]) == 0:
            self.index += 1

        if not self.tokens_available():
            return None

        try:
            item = float(self.parameters[self.index])
        except ValueError:
            item = self.parameters[self.index]

        self.index += 1
        return item

    def parse_numbers(self):
        self.index -= 1
        self.parse_line_to(self.relative)

    def parse_move_to(self, relative):
        x = self.next_token()
        y = self.next_token()

        if not isinstance(x, float) or not isinstance(y, float):
            return

        self.relative = relative
        self.commands.append(MoveTo(x, y, relative))

    def parse_line_to(self, relative):
        x = self.next_token()
        y = self.next_token()

        if not isinstance(x, float) or not isinstance(y, float):
            return

        self.commands.append(LineTo(x, y, relative))

    def parse_cubic_curve(self, relative):
        x1 = self.next_token()
        y1 = self.next_token()
        x2 = self.next_token()
        y2 = self.next_token()
        x = self.next_token()
        y = self.next_token()

        if not isinstance(x, float) or not isinstance(y, float) \
                or not isinstance(x1, float) or not isinstance(y1, float) \
                or not isinstance(x2, float) or not isinstance(y2, float):
            return

        self.previous_control = (x2, y2)

        self.commands.append(CubicCurve(x1, y1, x2, y2, x, y, relative))

    def parse_smooth_cubic(self, relative):
        x2 = self.next_token()
        y2 = self.next_token()
        x = self.next_token()
        y = self.next_token()

        if not isinstance(x, float) or not isinstance(y, float) \
                or not isinstance(x2, float) or not isinstance(y2, float):
            return

        self.commands.append(SmoothCubicCurve(x2, y2, x, y, relative))

    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "path"):
            return None

        if "d" in element.keys():
            d = element.get("d").replace(",", " ")
        else: return None

        self.commands = []
        self.parameters = d.split(" ")
        self.index = 0
        while self.tokens_available():
            parameter = self.next_token()

            if isinstance(parameter, float):
                self.parse_numbers()

            elif "mM".find(parameter) != -1:
                self.parse_move_to(parameter == "m")

            elif "lL".find(parameter) != -1:
                self.parse_move_to(parameter == "l")

            elif "cC".find(parameter) != -1:
                self.parse_cubic_curve(parameter == "c")

            elif "sS".find(parameter) != -1:
                self.parse_smooth_cubic(parameter == "s")

            else: break

        return Path(self.commands, config)