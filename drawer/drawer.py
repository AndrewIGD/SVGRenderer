from math import floor
from PIL import Image, ImageDraw

class SVGConfig:
    def __init__(self, pixels_per_mm):
        self.pixels_per_mm = pixels_per_mm
        self.image = None

class Drawable:
    def __init__(self, x, y, width, height, config):
        self.x = floor(x * config.pixels_per_mm)
        self.y = floor(y * config.pixels_per_mm)
        self.width = floor(width * config.pixels_per_mm)
        self.height = floor(height * config.pixels_per_mm)
        self.config = config

    def draw(self):
        pass