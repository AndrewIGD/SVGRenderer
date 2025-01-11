class Arc:
    def __init__(self, x, y, rx, ry, x_rotation, large_arc, sweep, relative):
        """
        Initializes a new arc to be drawn.

        Args:
            x (float): the end position of the arc
            y (float): the start position of the arc
            rx (float): the x rotation of the arc
            ry (float): the y rotation of the arc
            x_rotation (float): the rotation of the arc
            large_arc (float): if the arc should be the larger of the smaller one
            sweep (float): if the arc should be drawn counter-clockwise or not
            relative (float): if the end position is relative to the start position
        """
        self.rx = rx
        self.ry = ry
        self.x_rotation = x_rotation
        self.large_arc = large_arc
        self.sweep = sweep
        self.x = x
        self.y = y
        self.relative = relative