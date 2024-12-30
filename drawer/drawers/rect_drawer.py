from math import floor

from drawer.drawer import Drawable
from drawer.drawers.path_commands.arc import Arc
from drawer.drawers.path_commands.close_path import ClosePath
from drawer.drawers.path_commands.line_to import LineTo
from drawer.drawers.path_commands.move_to import MoveTo
from drawer.drawers.path_drawer import Path


class Rectangle(Drawable):
    def __init__(self, x, y, width, height, rx, ry, config, fill, outline, outline_width):
        super().__init__(x, y, width, height, config, fill, outline, outline_width)
        self.rx = floor(rx * config.pixels_per_mm)
        self.ry = floor(ry * config.pixels_per_mm)

    def draw(self):
        ppm = self.config.pixels_per_mm
        rect_x0, rect_y0 = self.x / ppm, self.y / ppm
        rect_x1, rect_y1 = (self.x + self.width) / ppm, (self.y + self.height) / ppm

        rx = self.rx / ppm
        ry = self.ry / ppm

        path = Path([
            MoveTo(rect_x0, rect_y0 + ry, False),
            Arc(rect_x0 + rx, rect_y0, rx, ry, 0, True, False, False),
            LineTo(rect_x1, rect_y0, False),
            LineTo(rect_x1, rect_y1, False),
            LineTo(rect_x0, rect_y1, False),
            ClosePath()
        ], self.config, "#FFFFFF", "#000000", 1)
        path.draw()