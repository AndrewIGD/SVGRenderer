class CubicCurve:
    def __init__(self, x1, y1, x2, y2, x, y, relative):
        """
        Initializes a cubic curve to be drawn.

        Args:
            x1 (float): the x position of the first control point
            y1 (float): the y position of the first control point
            x2 (float): the x position of the second control point
            y2 (float): the y position of the second control point
            x (float): the x end position
            y (float): the y end position
            relative (float): if the end position is relative to the start position
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y
        self.relative = relative