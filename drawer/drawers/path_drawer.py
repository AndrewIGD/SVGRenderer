from math import floor

from drawer.drawer import Drawable
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


class Path(Drawable):
    def __init__(self, commands, config):
        super().__init__(0, 0, 0, 0, config)
        self.commands = commands
        self.previous_cubic_control = None
        self.previous_quadratic_control = None
        self.path_started = False
        self.path_start_point = None

    def set_start_point(self, x, y):
        if self.path_started:
            return

        self.path_started = True
        self.path_start_point = (x, y)

    def draw_cubic(self, start, control1, control2, end):
        def cubic_bezier(p0, p1, p2, p3, t):
            return (
                (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 *
                p3[0],
                (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 *
                p3[1],
            )

        image = self.config.image

        points = [cubic_bezier(start, control1, control2, end, t) for t in [i / 100 for i in range(101)]]

        image.line(points, fill="black", width=self.config.pixels_per_mm)

        self.previous_cubic_control = control2

    def draw_quadratic(self, start, control, end):
        def quadratic_bezier(p0, p1, p2, t):
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            return x, y

        image = self.config.image

        points = [quadratic_bezier(start, control, end, t) for t in [i / 100 for i in range(101)]]

        image.line(points, fill="black", width=self.config.pixels_per_mm)

        self.previous_quadratic_control = control

    def draw(self):
        image = self.config.image

        x = 0
        y = 0

        for command in self.commands:
            if isinstance(command, MoveTo):
                if command.relative:
                    x += command.x * self.config.pixels_per_mm
                    y += command.y * self.config.pixels_per_mm
                else:
                    x = command.x * self.config.pixels_per_mm
                    y = command.y * self.config.pixels_per_mm

            elif isinstance(command, LineTo):
                if command.relative:
                    new_x = x + command.x * self.config.pixels_per_mm
                    new_y = y + command.y * self.config.pixels_per_mm
                else:
                    new_x = command.x * self.config.pixels_per_mm
                    new_y = command.y * self.config.pixels_per_mm

                image.line([(x, y), (new_x, new_y)], fill="black", width=self.config.pixels_per_mm)

                self.set_start_point(x, y)

                x = new_x
                y = new_y

            elif isinstance(command, HorizontalLine):
                if command.relative:
                    new_x = x + command.x * self.config.pixels_per_mm
                else:
                    new_x = command.x * self.config.pixels_per_mm

                image.line([(x, y), (new_x, y)], fill="black", width=self.config.pixels_per_mm)

                self.set_start_point(x, y)

                x = new_x

            elif isinstance(command, VerticalLine):
                if command.relative:
                    new_y = y + command.y * self.config.pixels_per_mm
                else:
                    new_y = command.y * self.config.pixels_per_mm

                image.line([(x, y), (x, new_y)], fill="black", width=self.config.pixels_per_mm)

                self.set_start_point(x, y)

                y = new_y

            elif isinstance(command, CubicCurve):
                start = (x, y)
                if command.relative:
                    control1 = (x + command.x1 * self.config.pixels_per_mm, y + command.y1 * self.config.pixels_per_mm)
                    control2 = (x + command.x2 * self.config.pixels_per_mm, y + command.y2 * self.config.pixels_per_mm)
                    end = (x + command.x * self.config.pixels_per_mm, y + command.y * self.config.pixels_per_mm)
                else:
                    control1 = (command.x1 * self.config.pixels_per_mm, command.y1 * self.config.pixels_per_mm)
                    control2 = (command.x2 * self.config.pixels_per_mm, command.y2 * self.config.pixels_per_mm)
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                self.draw_cubic(start, control1, control2, end)

                self.set_start_point(x, y)

                x = end[0]
                y = end[1]

            elif isinstance(command, SmoothCubicCurve):
                start = (x, y)
                if command.relative:
                    control2 = (x + command.x2 * self.config.pixels_per_mm, y + command.y2 * self.config.pixels_per_mm)
                    end = (x + command.x * self.config.pixels_per_mm, y + command.y * self.config.pixels_per_mm)
                else:
                    control2 = (command.x2 * self.config.pixels_per_mm, command.y2 * self.config.pixels_per_mm)
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                if self.previous_cubic_control is None:
                    control1 = start
                else:
                    control1 = self.previous_cubic_control

                self.draw_cubic(start, (2 * start[0] - control1[0], 2 * start[1] - control1[1]), control2, end)

                self.set_start_point(x, y)

                x = end[0]
                y = end[1]

            elif isinstance(command, QuadraticCurve):
                start = (x, y)
                if command.relative:
                    control = (x + command.x1 * self.config.pixels_per_mm, y + command.y1 * self.config.pixels_per_mm)
                    end = (x + command.x * self.config.pixels_per_mm, y + command.y * self.config.pixels_per_mm)
                else:
                    control = (command.x1 * self.config.pixels_per_mm, command.y1 * self.config.pixels_per_mm)
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                self.draw_quadratic(start, control, end)

                self.set_start_point(x, y)

                x = end[0]
                y = end[1]

            elif isinstance(command, SmoothQuadraticCurve):
                start = (x, y)
                if command.relative:
                    end = (x + command.x * self.config.pixels_per_mm, y + command.y * self.config.pixels_per_mm)
                else:
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                if self.previous_quadratic_control is None:
                    control = start
                else:
                    control = self.previous_quadratic_control

                self.draw_quadratic(start, (2 * start[0] - control[0], 2 * start[1] - control[1]), end)

                self.set_start_point(x, y)

                x = end[0]
                y = end[1]

            elif isinstance(command, Arc):
                pass

            elif isinstance(command, ClosePath):
                image.line([(x, y), self.path_start_point], fill="black", width=self.config.pixels_per_mm)
                return
