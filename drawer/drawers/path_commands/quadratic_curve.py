class QuadraticCurve:
    def __init__(self, x1, y1, x, y, relative):
        """
        Initializes a quadratic curve to be drawn.

        Args:
            x1 (float): the x position of the control point
            y1 (float): the y position of the control point
            x (float): the x end position
            y (float): the y end position
            relative (float): if the end position is relative to the start position
        """
        self.x1 = x1
        self.y1 = y1
        self.x = x
        self.y = y
        self.relative = relative