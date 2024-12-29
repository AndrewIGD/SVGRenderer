from drawer.drawer import Drawable

class Arc(Drawable):
    def __init__(self, x, y, rx, ry, x_rotation, large_arc, sweep, relative, fill, outline, outline_width, width,
                 height, config):
        super().__init__(x, y, width, height, config)
        self.rx = rx
        self.ry = ry
        self.x_rotation = x_rotation
        self.large_arc = large_arc
        self.sweep = sweep
        self.x = x
        self.y = y
        self.relative = relative