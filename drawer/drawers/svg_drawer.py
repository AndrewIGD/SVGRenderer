from PIL import Image, ImageDraw

from drawer.drawers.group_drawer import Group

class SVG(Group):
    def __init__(self, x, y, width, height, config):
        """
           Initializes an SVG drawer.

           Args:
               x (float): the x position of the view box
               y (float): the y position of the view box
               width (float): the width of the view box
               height (float): the height of the view box
               config (Config): the configuration of the SVG drawer
        """

        super().__init__(x, y, width, height, config)
        self.image = None

    def draw(self):
        """
           Draws the entire SVG file onto the canvas.
        """

        self.image = Image.new("RGB", (self.width, self.height), "white")
        self.config.image = ImageDraw.Draw(self.image)
        for child in self.children:
            child.draw()

    def get_image(self):
        """
           Returns:
               Image: an image with the SVG rendered on it
        """

        self.draw()
        return self.image