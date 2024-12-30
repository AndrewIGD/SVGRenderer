import math
from math import floor

from drawer.drawer import Drawable


class Line(Drawable):
    def __init__(self, x1, y1, x2, y2, config, stroke, stroke_width):
        super().__init__(0, 0, 0, 0, config, outline=stroke, outline_width=stroke_width)
        self.x1 = floor(x1 * config.pixels_per_mm)
        self.x2 = floor(x2 * config.pixels_per_mm)
        self.y1 = floor(y1 * config.pixels_per_mm)
        self.y2 = floor(y2 * config.pixels_per_mm)

    def draw(self):
        image = self.config.image

        image.line([(self.x1, self.y1), (self.x2, self.y2)], fill=self.outline, width=math.floor(self.outline_width * self.config.pixels_per_mm))