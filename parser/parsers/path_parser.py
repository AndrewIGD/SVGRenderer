from xml.etree.ElementTree import Element

from drawer.drawer import SVGConfig
from drawer.drawers.path_commands.arc import Arc
from drawer.drawers.path_commands.close_path import ClosePath
from drawer.drawers.path_commands.cubic_curve import CubicCurve
from drawer.drawers.path_commands.horizontal_line import HorizontalLine
from drawer.drawers.path_commands.line_to import LineTo
from drawer.drawers.path_commands.move_to import MoveTo
from drawer.drawers.path_commands.quadratic_curve import QuadraticCurve
from drawer.drawers.path_commands.smooth_cubic import SmoothCubicCurve
from drawer.drawers.path_commands.smooth_quadratic import SmoothQuadraticCurve
from drawer.drawers.path_commands.vertical_line import VerticalLine
from drawer.drawers.path_drawer import Path
from parser.parsers.parser_base import Parser
from parser.shape_parser import ShapeParser
from parser.utils import compare_tag


class PathParser(ShapeParser):
    def __init__(self):
        super().__init__()
        self.parameters = []
        self.index = 0
        self.commands = []
        self.relative = False

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

    def parse_h_line(self, relative):
        x = self.next_token()

        if not isinstance(x, float):
            return

        self.commands.append(HorizontalLine(x, relative))

    def parse_v_line(self, relative):
        y = self.next_token()

        if not isinstance(y, float):
            return

        self.commands.append(VerticalLine(y, relative))

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

    def parse_quadratic_curve(self, relative):
        x1 = self.next_token()
        y1 = self.next_token()
        x = self.next_token()
        y = self.next_token()

        if not isinstance(x, float) or not isinstance(y, float) \
                or not isinstance(x1, float) or not isinstance(y1, float):
            return

        self.commands.append(QuadraticCurve(x1, y1, x, y, relative))

    def parse_smooth_quadratic(self, relative):
        x = self.next_token()
        y = self.next_token()

        if not isinstance(x, float) or not isinstance(y, float):
            return

        self.commands.append(SmoothQuadraticCurve(x, y, relative))

    def parse_arc(self, relative):
        rx = self.next_token()
        ry = self.next_token()
        x_rotation = self.next_token()
        large_arc = self.next_token()
        sweep = self.next_token()
        x = self.next_token()
        y = self.next_token()

        if (not isinstance(x, float) or not isinstance(y, float)
                or not isinstance(rx, float) or not isinstance(ry, float)
                or not isinstance(x_rotation, float)
                or not isinstance(large_arc, float) or not isinstance(sweep, float)):
            return

        self.commands.append(Arc(x, y, rx, ry, x_rotation, large_arc, sweep, relative))

    def parse_close_path(self):
        self.commands.append(ClosePath())

    def try_parse(self, element: Element, config: SVGConfig):
        if not compare_tag(element, "path"):
            return None

        self.parse_shape_elements(element)

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
                self.parse_line_to(parameter == "l")

            elif "hH".find(parameter) != -1:
                self.parse_h_line(parameter == "h")

            elif "vV".find(parameter) != -1:
                self.parse_v_line(parameter == "v")

            elif "cC".find(parameter) != -1:
                self.parse_cubic_curve(parameter == "c")

            elif "sS".find(parameter) != -1:
                self.parse_smooth_cubic(parameter == "s")

            elif "qQ".find(parameter) != -1:
                self.parse_quadratic_curve(parameter == "q")

            elif "tT".find(parameter) != -1:
                self.parse_smooth_quadratic(parameter == "t")

            elif "aA".find(parameter) != -1:
                self.parse_arc(parameter == "a")

            elif "zZ".find(parameter) != -1:
                self.parse_close_path()

            else: break

        return Path(self.commands, config, self.fill, self.outline, self.outline_width)