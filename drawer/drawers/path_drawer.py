import math
from math import radians

from drawer.drawer import Drawable
from drawer.drawers.common.outline import outline
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
        """
           Initializes a path drawer.

           Args:
               commands (list): the list of commands that define a shape
               config (Config): the drawing configuration of the shape
               fill (string): the fill hex color of the shape
               outline (string): the outline hex color of the shape
               outline_width (float): the outline width of the shape
        """
        super().__init__(0, 0, 0, 0, config, fill, outline, outline_width)
        self.commands = commands
        self.previous_cubic_control = None
        self.previous_quadratic_control = None
        self.polygons = []
        self.current_polygon = []
        self.x = 0
        self.y = 0

    def add_points_to_polygon(self, points):
        """
           Appends a list of points to the current polygon.

           Args:
               points (list): the list of points
        """

        if len(self.current_polygon) == 0:
            self.current_polygon.append((self.x, self.y))

        self.current_polygon.extend(points)

    def draw_cubic(self, start, control1, control2, end):
        """"
           Draws a cubic bezier curve.

           Args:
               start(tuple): the start position
               control1(tuple): the first control position
               control2(tuple): the second control position
               end(tuple): the end position
        """

        def cubic_bezier(p0, p1, p2, p3, t):
            """"
               Cubic bezier function.

               Args:
                   p0 (tuple): the start position
                   p1 (tuple): the first control position
                   p2 (tuple): the second control position
                   p3 (tuple): the end position
                   t (float): function parameter. Ranges from 0 to 1

                Returns:
                    tuple: point on the cubic bezier curve
            """

            return (
                (1 - t) ** 3 * p0[0] + 3 * (1 - t) ** 2 * t * p1[0] + 3 * (1 - t) * t ** 2 * p2[0] + t ** 3 *
                p3[0],
                (1 - t) ** 3 * p0[1] + 3 * (1 - t) ** 2 * t * p1[1] + 3 * (1 - t) * t ** 2 * p2[1] + t ** 3 *
                p3[1],
            )

        point_count = 50 * self.config.pixels_per_mm
        points = [cubic_bezier(start, control1, control2, end, t) for t in [i / point_count for i in range(point_count + 1)]]

        self.add_points_to_polygon(points)

        self.previous_cubic_control = control2

    def draw_quadratic(self, start, control, end):
        """"
           Draws a quadratic bezier curve.

           Args:
               start(tuple): the start position
               control(tuple): the control position
               end(tuple): the end position
        """

        def quadratic_bezier(p0, p1, p2, t):
            """"
                Quadratic bezier function.

                Args:
                    p0 (tuple): the start position
                    p1 (tuple): the control position
                    p2 (tuple): the end position
                    t (float): function parameter. Ranges from 0 to 1

                Returns:
                    tuple: point on the quadratic bezier curve
            """

            x = (1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t ** 2 * p2[0]
            y = (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t ** 2 * p2[1]
            return x, y

        point_count = 50 * self.config.pixels_per_mm
        points = [quadratic_bezier(start, control, end, t) for t in [i / point_count for i in range(point_count + 1)]]

        self.add_points_to_polygon(points)

        self.previous_quadratic_control = control

    def draw_arc(self, cx, cy, rx, ry, start_angle, end_angle, angle, sweep):
        """"
           Draws an elliptical arc.

           Args:
               cx (float): the center x coordinate
               cy (float): the center y coordinate
               rx (float): the x radius of the arc
               ry (float): the x radius of the arc
               start_angle (float): the start angle of the arc
               end_angle (float): the end angle of the arc
               angle (float): the rotation of the arc
               sweep (float): the sweep flag of the arc
        """

        def ellipse(t):
            """"
                Ellipse function.

                Args:
                    t (float): function parameter. Ranges from 0 to 1

                Returns:
                    tuple: point on the ellipse
            """

            ellipse_point = cx + rx * math.cos(t), cy + ry * math.sin(t)

            angle_radians = math.radians(angle)

            x_new = cx + (ellipse_point[0] - cx) * math.cos(angle_radians) - (ellipse_point[1] - cy) * math.sin(angle_radians)
            y_new = cy + (ellipse_point[0] - cx) * math.sin(angle_radians) + (ellipse_point[1] - cy) * math.cos(angle_radians)

            return x_new, y_new

        def frange(start, stop, reverse):
            index = start
            nums = []
            step = 10
            if reverse:
                step = -10

            while (index <= stop) != reverse:
                nums.append(index)
                index += step

            nums.append(stop)
            return nums

        points = [ellipse(t) for t in [math.radians(i) for i in frange(start_angle, end_angle, start_angle > end_angle)]]

        if not sweep:
            points.reverse()

        self.add_points_to_polygon(points)

    def draw(self):
        """
        Draws the path on the canvas given by the configuration.
        """

        image = self.config.image

        for command in self.commands:
            if isinstance(command, MoveTo):

                if len(self.current_polygon) > 1:
                    self.polygons.append(self.current_polygon)

                self.current_polygon = []

                if command.relative:
                    self.x += command.x * self.config.pixels_per_mm
                    self.y += command.y * self.config.pixels_per_mm
                else:
                    self.x = command.x * self.config.pixels_per_mm
                    self.y = command.y * self.config.pixels_per_mm

            elif isinstance(command, LineTo):
                if command.relative:
                    new_x = self.x + command.x * self.config.pixels_per_mm
                    new_y = self.y + command.y * self.config.pixels_per_mm
                else:
                    new_x = command.x * self.config.pixels_per_mm
                    new_y = command.y * self.config.pixels_per_mm

                self.add_points_to_polygon([(new_x, new_y)])

                self.x = new_x
                self.y = new_y

            elif isinstance(command, HorizontalLine):
                if command.relative:
                    new_x = self.x + command.x * self.config.pixels_per_mm
                else:
                    new_x = command.x * self.config.pixels_per_mm

                self.add_points_to_polygon([(new_x, self.y)])

                self.x = new_x

            elif isinstance(command, VerticalLine):
                if command.relative:
                    new_y = self.y + command.y * self.config.pixels_per_mm
                else:
                    new_y = command.y * self.config.pixels_per_mm

                self.add_points_to_polygon([(self.x, new_y)])

                self.y = new_y

            elif isinstance(command, CubicCurve):
                start = (self.x, self.y)
                if command.relative:
                    control1 = (self.x + command.x1 * self.config.pixels_per_mm, self.y + command.y1 * self.config.pixels_per_mm)
                    control2 = (self.x + command.x2 * self.config.pixels_per_mm, self.y + command.y2 * self.config.pixels_per_mm)
                    end = (self.x + command.x * self.config.pixels_per_mm, self.y + command.y * self.config.pixels_per_mm)
                else:
                    control1 = (command.x1 * self.config.pixels_per_mm, command.y1 * self.config.pixels_per_mm)
                    control2 = (command.x2 * self.config.pixels_per_mm, command.y2 * self.config.pixels_per_mm)
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                self.draw_cubic(start, control1, control2, end)

                self.x = end[0]
                self.y = end[1]

            elif isinstance(command, SmoothCubicCurve):
                start = (self.x, self.y)
                if command.relative:
                    control2 = (self.x + command.x2 * self.config.pixels_per_mm, self.y + command.y2 * self.config.pixels_per_mm)
                    end = (self.x + command.x * self.config.pixels_per_mm, self.y + command.y * self.config.pixels_per_mm)
                else:
                    control2 = (command.x2 * self.config.pixels_per_mm, command.y2 * self.config.pixels_per_mm)
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                if self.previous_cubic_control is None:
                    control1 = start
                else:
                    control1 = self.previous_cubic_control

                self.draw_cubic(start, (2 * start[0] - control1[0], 2 * start[1] - control1[1]), control2, end)

                self.x = end[0]
                self.y = end[1]

            elif isinstance(command, QuadraticCurve):
                start = (self.x, self.y)
                if command.relative:
                    control = (self.x + command.x1 * self.config.pixels_per_mm, self.y + command.y1 * self.config.pixels_per_mm)
                    end = (self.x + command.x * self.config.pixels_per_mm, self.y + command.y * self.config.pixels_per_mm)
                else:
                    control = (command.x1 * self.config.pixels_per_mm, command.y1 * self.config.pixels_per_mm)
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                self.draw_quadratic(start, control, end)

                self.x = end[0]
                self.y = end[1]

            elif isinstance(command, SmoothQuadraticCurve):
                start = (self.x, self.y)
                if command.relative:
                    end = (self.x + command.x * self.config.pixels_per_mm, self.y + command.y * self.config.pixels_per_mm)
                else:
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                if self.previous_quadratic_control is None:
                    control = start
                else:
                    control = self.previous_quadratic_control

                self.draw_quadratic(start, (2 * start[0] - control[0], 2 * start[1] - control[1]), end)

                self.x = end[0]
                self.y = end[1]

            elif isinstance(command, Arc):
                if command.rx < 0: command.rx = -command.rx
                if command.ry < 0: command.ry = -command.ry

                command.rx *= self.config.pixels_per_mm
                command.ry *= self.config.pixels_per_mm

                start = (self.x, self.y)
                if command.relative:
                    end = (self.x + command.x * self.config.pixels_per_mm, self.y + command.y * self.config.pixels_per_mm)
                else:
                    end = (command.x * self.config.pixels_per_mm, command.y * self.config.pixels_per_mm)

                if command.rx == 0 or command.ry == 0:
                    self.add_points_to_polygon([end])
                    self.x = end[0]
                    self.y = end[1]
                    continue

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

                if end_angle < start_angle:
                    end_angle += 360

                self.draw_arc(cx, cy, command.rx, command.ry, start_angle, end_angle, command.x_rotation, command.sweep)

                self.x = end[0]
                self.y = end[1]

            elif isinstance(command, ClosePath):
                if len(self.current_polygon) <= 1:
                    self.current_polygon = []
                    continue

                first_point = self.current_polygon[0]

                self.add_points_to_polygon([first_point])
                self.polygons.append(self.current_polygon)
                self.current_polygon = []

                self.x = first_point[0]
                self.y = first_point[1]


        if len(self.current_polygon) > 1:
            self.polygons.append(self.current_polygon)

        for polygon in self.polygons:
            image.polygon(polygon, fill=self.fill, width=0)
            outline(self.config, polygon, color=self.outline, width=math.floor(self.outline_width * self.config.pixels_per_mm))