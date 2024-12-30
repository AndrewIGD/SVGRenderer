import math

from drawer.drawer import Drawable
from drawer.drawers.common.outline import outline


class Polyline(Drawable):
    def __init__(self, points, config, fill, outline, outline_width):
        super().__init__(0, 0, 0, 0, config, fill, outline, outline_width)
        self.points = []
        for point in points:
            self.points.append((float(point[0]) * config.pixels_per_mm, float(point[1]) * config.pixels_per_mm))

    def draw(self):
        image = self.config.image

        image.polygon(self.points, fill=self.fill, width=0)

        if self.outline is None:
            return

        outline(self.config, self.points, self.outline, math.floor(self.outline_width * self.config.pixels_per_mm))