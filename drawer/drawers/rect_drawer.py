from drawer.drawer import Drawable


class Rectangle(Drawable):
    def __init__(self, x, y, width, height, rx, ry, config):
        super().__init__(x, y, width, height, config)
        self.rx = rx
        self.ry = ry

    def draw(self):
        image = self.config.image
        image.rectangle([self.x, self.y, self.x + self.width, self.y + self.height], fill="black")