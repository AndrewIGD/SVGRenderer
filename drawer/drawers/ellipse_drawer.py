import math
from math import floor

from drawer.drawer import Drawable


class Ellipse(Drawable):
    def __init__(self, cx, cy, rx, ry, config, fill, outline, outline_width):
        """
           Initializes an ellipse drawer.

           Args:
               cx (float): the x center position of the ellipse
               cy (float): the y center position of the ellipse
               rx (float): the x radius of the ellipse
               ry (float): the y radius of the ellipse
               config (Config): the drawing configuration of the ellipse
               fill (string): the fill hex color of the ellipse
               outline (string): the outline hex color of the ellipse
               outline_width (float): the outline width of the ellipse
        """
        super().__init__(0, 0, 0, 0, config, fill, outline, outline_width)
        self.cx = floor(cx * config.pixels_per_mm)
        self.cy = floor(cy * config.pixels_per_mm)
        self.rx = floor(rx * config.pixels_per_mm)
        self.ry = floor(ry * config.pixels_per_mm)

    def draw(self):
        """
            Draws the ellipse on the canvas given by the configuration.
        """

        image = self.config.image

        bounding_box = [self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry]

        image.ellipse(bounding_box, fill=self.fill, outline=self.outline, width=math.floor(self.outline_width * self.config.pixels_per_mm))