class SmoothCubicCurve:
    def __init__(self, x2, y2, x, y, relative):
        """
        Initializes a smooth cubic curve to be drawn. This means that the first control point is symmetrical to the previous cubic curve's second control point.

        Args:
            x2 (float): the x position of the second control point
            y2 (float): the y position of the second control point
            x (float): the x end position
            y (float): the y end position
            relative (float): if the end position is relative to the start position
        """
        self.x2 = x2
        self.y2 = y2
        self.x = x
        self.y = y
        self.relative = relative