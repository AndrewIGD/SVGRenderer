class MoveTo:
    def __init__(self, x, y, relative):
        """
        Initializes a move to command, which moves the cursor without drawing a line.

        Args:
            x (float): the x position of the cursor
            y (float): the y position of the cursor
            relative (float): if the new position is relative to the current position
        """
        self.x = x
        self.y = y
        self.relative = relative