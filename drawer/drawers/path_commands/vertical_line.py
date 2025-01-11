class VerticalLine:
    def __init__(self, y, relative):
        """
        Initializes a vertical line to be drawn.

        Args:
            y (float): the y delta of the line
            relative (float): if the end position is relative to the start position
        """
        self.y = y
        self.relative = relative