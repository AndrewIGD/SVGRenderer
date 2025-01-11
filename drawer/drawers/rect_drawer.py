from math import floor

from drawer.drawer import Drawable
from drawer.drawers.path_commands.arc import Arc
from drawer.drawers.path_commands.close_path import ClosePath
from drawer.drawers.path_commands.line_to import LineTo
from drawer.drawers.path_commands.move_to import MoveTo
from drawer.drawers.path_drawer import Path


class Rectangle(Drawable):
    def __init__(self, x, y, width, height, rx, ry, config, fill, outline, outline_width):
        """
           Initializes a rectangle drawer.

           Args:
               x (float): the x position of the rectangle
               y (float): the y position of the rectangle
               width (float): the width of the rectangle
               height (float): the height of the rectangle
               rx (float): the x radius of the rectangle
               ry (float): the y radius of the rectangle
               config (Config): the drawing configuration of the rectangle
               fill (string): the fill hex color of the rectangle
               outline (string): the outline hex color of the rectangle
               outline_width (float): the outline width of the rectangle
        """

        super().__init__(x, y, width, height, config, fill, outline, outline_width)
        self.rx = floor(rx * config.pixels_per_mm)
        self.ry = floor(ry * config.pixels_per_mm)

    def draw(self):
        """
        Draws the rectangle on the canvas given by the configuration.
        """

        ppm = self.config.pixels_per_mm
        x, y = self.x / ppm, self.y / ppm
        width, height = self.width / ppm, self.height / ppm

        rx = self.rx / ppm
        ry = self.ry / ppm

        path = Path([
            MoveTo(x, y + ry, False),
            Arc(rx, -ry, rx, ry, 0, False, True, True),
            LineTo(width - 2 * rx, 0, True),
            Arc(rx, ry, rx, ry, 0, False, True, True),
            LineTo(0, height - 2 * ry, True),
            Arc(-rx, ry, rx, ry, 0, False, True, True),
            LineTo(-width + 2 * rx, 0, True),
            Arc(-rx, -ry, rx, ry, 0, False, True, True),
            ClosePath()
        ], self.config, self.fill, self.outline, self.outline_width)
        path.draw()