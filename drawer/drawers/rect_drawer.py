from math import floor

from drawer.drawer import Drawable


class Rectangle(Drawable):
    def __init__(self, x, y, width, height, rx, ry, config, fill, outline, outline_width):
        super().__init__(x, y, width, height, config, fill, outline, outline_width)
        self.rx = floor(rx * config.pixels_per_mm)
        self.ry = floor(ry * config.pixels_per_mm)

    def draw(self):
        image = self.config.image
        rect_x0, rect_y0 = self.x, self.y
        rect_x1, rect_y1 = self.x + self.width, self.y + self.height

        fill_color = self.outline
        width = self.outline_width * self.config.pixels_per_mm

        image.arc([rect_x0, rect_y0, rect_x0 + self.rx * 2, rect_y0 + self.ry * 2],
                 start=180, end=270, fill=fill_color, width=width)
        image.arc([rect_x1 - self.rx * 2, rect_y0, rect_x1, rect_y0 + self.ry * 2],
                 start=270, end=360, fill=fill_color, width=width)
        image.arc([rect_x1 - self.rx * 2, rect_y1 - self.ry * 2, rect_x1, rect_y1],
                 start=0, end=90, fill=fill_color, width=width)
        image.arc([rect_x0, rect_y1 - self.ry * 2, rect_x0 + self.rx * 2, rect_y1],
                 start=90, end=180, fill=fill_color, width=width)

        image.line([rect_x0 + self.rx, rect_y0, rect_x1 - self.rx, rect_y0], fill=fill_color, width=width)
        image.line([rect_x1, rect_y0 + self.ry, rect_x1, rect_y1 - self.ry], fill=fill_color, width=width)
        image.line([rect_x0 + self.rx, rect_y1, rect_x1 - self.rx, rect_y1], fill=fill_color, width=width)
        image.line([rect_x0, rect_y0 + self.ry, rect_x0, rect_y1 - self.ry], fill=fill_color, width=width)