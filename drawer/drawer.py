from math import floor
from PIL import Image, ImageDraw

class SVGConfig:
    def __init__(self, pixels_per_mm):
        self.pixels_per_mm = pixels_per_mm
        self.image = None

class Drawable:
    def __init__(self, x, y, width, height, config):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.config = config

    def get_width(self):
        return floor(self.width * self.config.pixels_per_mm)

    def get_height(self):
        return floor(self.height * self.config.pixels_per_mm)

    def draw(self):
        pass