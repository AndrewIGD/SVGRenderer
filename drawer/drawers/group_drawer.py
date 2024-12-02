from drawer.drawer import Drawable

class Group(Drawable):
    def __init__(self, x, y, width, height, config):
        super().__init__(x, y, width, height, config)
        self.children = []

    def add_child(self, drawable: Drawable):
        self.children.append(drawable)