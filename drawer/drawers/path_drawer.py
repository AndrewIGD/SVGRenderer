import math
from math import floor, radians

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
    def __init__(self, commands, config, fill, outline, outline_width):
        super().__init__(0, 0, 0, 0, config, fill, outline, outline_width)
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

        image.polygon(points, fill=self.fill, outline=self.outline ,width=self.outline_width * self.config.pixels_per_mm)

        self.previous_cubic_control = control2

    def draw_quadratic(self, start, control, end):
        def quadratic_bezier(p0, p1, p2, t):
            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            return x, y

        image = self.config.image

        points = [quadratic_bezier(start, control, end, t) for t in [i / 100 for i in range(101)]]

        image.polygon(points, fill=self.fill, outline=self.outline ,width=self.outline_width * self.config.pixels_per_mm)

        self.previous_quadratic_control = control

    def draw_arc(self, cx, cy, rx, ry, start_angle, end_angle, angle):
        def ellipse(t):
            ellipse_point = cx + rx * math.cos(t), cy + ry * math.sin(t)

            angle_radians = math.radians(angle)

            x_new = cx + (ellipse_point[0] - cx) * math.cos(angle_radians) - (ellipse_point[1] - cy) * math.sin(angle_radians)
            y_new = cy + (ellipse_point[0] - cx) * math.sin(angle_radians) + (ellipse_point[1] - cy) * math.cos(angle_radians)

            return x_new, y_new

        def frange(start, stop, step):
            index = start
            nums = []
            while index <= stop:
                nums.append(index)
                index += step

            nums.append(stop)
            return nums

        image = self.config.image

        points = [ellipse(t) for t in [math.radians(i) for i in frange(start_angle, end_angle, 1)]]

        image.polygon(points, fill="black", width=self.config.pixels_per_mm)

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

                image.line([(x, y), (new_x, new_y)], self.outline, width=self.config.pixels_per_mm)

                self.set_start_point(x, y)

                x = new_x
                y = new_y

            elif isinstance(command, HorizontalLine):
                if command.relative:
                    new_x = x + command.x * self.config.pixels_per_mm
                else:
                    new_x = command.x * self.config.pixels_per_mm

                image.line([(x, y), (new_x, y)], fill=self.outline, width=self.config.pixels_per_mm)

                self.set_start_point(x, y)

                x = new_x

            elif isinstance(command, VerticalLine):
                if command.relative:
                    new_y = y + command.y * self.config.pixels_per_mm
                else:
                    new_y = command.y * self.config.pixels_per_mm

                image.line([(x, y), (x, new_y)], fill=self.outline, width=self.config.pixels_per_mm)

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
                if command.rx == 0 or command.ry == 0: continue
                if command.rx < 0: command.rx = -command.rx
                if command.ry < 0: command.ry = -command.ry

                start = (x, y)
                if command.relative:
                    end = (x + command.x * self.config.pixels_per_mm, y + command.y * self.config.pixels_per_mm)
                else:
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                pi_times_2 = math.pi * 2
                phi = radians(command.x_rotation)

                sin_phi = math.sin(phi)
                cos_phi = math.cos(phi)

                hd_x = (start[0] - end[0]) / 2
                hd_y = (start[1] - end[1]) / 2
                hs_x = (start[0] + end[0]) / 2
                hs_y = (start[1] + end[1]) / 2

                x_prime = hd_x * cos_phi + sin_phi * hd_y
                y_prime = hd_y * cos_phi - sin_phi * hd_x

                lambda_ = math.pow(x_prime, 2) / math.pow(command.rx, 2) + math.pow(y_prime, 2) / math.pow(command.ry, 2)
                if lambda_ > 1:
                    command.rx = command.rx * math.sqrt(lambda_)
                    command.ry = command.ry * math.sqrt(lambda_)

                rxry = command.rx * command.ry
                rxyp = command.rx * y_prime
                ryxp = command.ry * x_prime
                sq_sum = math.pow(rxyp, 2) + math.pow(ryxp, 2)
                if sq_sum == 0:
                    continue

                coef = math.sqrt(abs((math.pow(rxry, 2) - sq_sum) / sq_sum))
                if command.large_arc == command.sweep:
                    coef = -coef

                cx_prime = coef * rxyp / command.ry
                cy_prime = -coef * ryxp / command.rx

                cx = cos_phi * cx_prime - sin_phi * cy_prime + hs_x
                cy = cos_phi * cy_prime + sin_phi * cx_prime + hs_y

                xcr1 = (x_prime - cx_prime) / command.rx
                xcr2 = (x_prime + cx_prime) / command.rx
                ycr1 = (y_prime - cy_prime) / command.ry
                ycr2 = (y_prime + cy_prime) / command.ry

                def angle_radians(ux, uy, vx, vy):
                    dot = ux * vx + uy * vy
                    mod = math.sqrt((math.pow(ux, 2) + math.pow(uy, 2)) * (math.pow(vx, 2) + math.pow(vy, 2)))
                    rad = math.acos(dot / mod)
                    if ux * vy - uy * vx < 0:
                        rad = -rad

                    return rad

                start_angle = angle_radians(1, 0, xcr1, ycr1)
                delta_angle = angle_radians(xcr1, ycr1, -xcr2, -ycr2)
                end_angle = start_angle + delta_angle

                start_angle = math.degrees(start_angle) % 360
                end_angle = math.degrees(end_angle) % 360

                if not command.sweep:
                    start_angle, end_angle = end_angle, start_angle

                if command.large_arc:
                    end_angle += 360

                self.draw_arc(cx, cy, command.rx, command.ry, start_angle, end_angle, command.x_rotation)

                x = end[0]
                y = end[1]

            elif isinstance(command, ClosePath):
                image.line([(x, y), self.path_start_point], fill=self.outline, width=self.config.pixels_per_mm)
                return
