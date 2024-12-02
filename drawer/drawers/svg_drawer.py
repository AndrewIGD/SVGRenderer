from PIL import Image, ImageDraw

from drawer.drawers.group_drawer import Group

class SVG(Group):
    def __init__(self, x, y, width, height, config):
        super().__init__(x, y, width, height, config)
        self.image = None

    def draw(self):
        self.image = Image.new("RGB", (self.get_width(), self.get_height()), "white")
        self.config.image = ImageDraw.Draw(self.image)
        for child in self.children:
            child.draw()

    def get_image(self):
        self.draw()
        return self.image