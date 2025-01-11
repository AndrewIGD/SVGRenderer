from math import floor
from PIL import Image, ImageDraw

class SVGConfig:
    def __init__(self, pixels_per_mm):
        """
           Initializes an SVG config.

           Args:
               pixels_per_mm (int): Number of pixels per millimeter
        """

        self.pixels_per_mm = pixels_per_mm
        self.image = None
        self.linecap = "curve"

class Drawable:
    def __init__(self, x, y, width, height, config, fill = None, outline = None, outline_width = None):
        """
           Initializes a shape drawer.

           Args:
               x (float): x position of the shape
               y (float): y position of the shape
               width (float): width of the shape
               height (float): height of the shape
               config (SVGConfig): Drawing settings
               fill (string): shape fill hex color
               outline (string): shape outline hex color
               outline_width (float): width of the shape outline
        """
        self.x = floor(x * config.pixels_per_mm)
        self.y = floor(y * config.pixels_per_mm)
        self.width = floor(width * config.pixels_per_mm)
        self.height = floor(height * config.pixels_per_mm)
        self.fill = fill
        self.outline = outline
        self.outline_width = outline_width
        self.config = config

    def draw(self):
        """
           Draws this drawable onto the given canvas in the config.
        """
        pass