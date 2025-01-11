import math
from math import floor

from drawer.drawer import Drawable


class Line(Drawable):
    def __init__(self, x1, y1, x2, y2, config, stroke, stroke_width):
        """
           Initializes a line drawer.

           Args:
               x1 (float): the x start position of the line
               y1 (float): the y start position of the line
               x2 (float): the x end position of the line
               y2 (float): the y end position of the line
               config (Config): the drawing configuration of the line
               stroke (string): the stroke hex color of the line
               stroke_width (float): the stroke width of the line
        """
        super().__init__(0, 0, 0, 0, config, outline=stroke, outline_width=stroke_width)
        self.x1 = floor(x1 * config.pixels_per_mm)
        self.x2 = floor(x2 * config.pixels_per_mm)
        self.y1 = floor(y1 * config.pixels_per_mm)
        self.y2 = floor(y2 * config.pixels_per_mm)

    def draw(self):
        """
        Draws the line on the canvas given by the configuration.
        """

        image = self.config.image

        image.line([(self.x1, self.y1), (self.x2, self.y2)], fill=self.outline, width=math.floor(self.outline_width * self.config.pixels_per_mm))