from math import floor

from drawer.drawer import Drawable


class Ellipse(Drawable):
    def __init__(self, cx, cy, rx, ry, config, fill, outline, outline_width):
        super().__init__(0, 0, 0, 0, config, fill, outline, outline_width)
        self.cx = floor(cx * config.pixels_per_mm)
        self.cy = floor(cy * config.pixels_per_mm)
        self.rx = floor(rx * config.pixels_per_mm)
        self.ry = floor(ry * config.pixels_per_mm)

    def draw(self):
        image = self.config.image

        bounding_box = [self.cx - self.rx, self.cy - self.ry, self.cx + self.rx, self.cy + self.ry]

        image.ellipse(bounding_box, fill=self.fill, outline=self.outline, width=self.outline_width * self.config.pixels_per_mm)