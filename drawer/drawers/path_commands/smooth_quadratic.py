class SmoothQuadraticCurve:
    def __init__(self, x, y, relative):
        """
        Initializes a smooth quadratic curve to be drawn. This means that the control point is symmetrical to the previous quadratic curve's control point.

        Args:
            x (float): the x end position
            y (float): the y end position
            relative (float): if the end position is relative to the start position
        """
        self.x = x
        self.y = y
        self.relative = relative