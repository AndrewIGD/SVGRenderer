class HorizontalLine:
    def __init__(self, x, relative):
        """
        Initializes a horizontal line to be drawn.

        Args:
            x (float): the x delta of the line
            relative (float): if the end position is relative to the start position
        """
        self.x = x
        self.relative = relative