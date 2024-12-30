from math import floor
from PIL import Image, ImageDraw

class SVGConfig:
    def __init__(self, pixels_per_mm):
        self.pixels_per_mm = pixels_per_mm
        self.image = None
        self.linecap = "curve"

class Drawable:
    def __init__(self, x, y, width, height, config, fill = None, outline = None, outline_width = None):
        self.x = floor(x * config.pixels_per_mm)
        self.y = floor(y * config.pixels_per_mm)
        self.width = floor(width * config.pixels_per_mm)
        self.height = floor(height * config.pixels_per_mm)
        self.fill = fill
        self.outline = outline
        self.outline_width = outline_width
        self.config = config

    def draw(self):
        pass