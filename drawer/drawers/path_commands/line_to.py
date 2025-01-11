class LineTo:
    def __init__(self, x, y, relative):
        """
        Initializes a line to be drawn.

        Args:
            x (float): the x end position of the line
            y (float): the y end position of the line
            relative (float): if the end position is relative to the start position
        """
        self.x = x
        self.y = y
        self.relative = relative