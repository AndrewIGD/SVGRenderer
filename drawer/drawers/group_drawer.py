from drawer.drawer import Drawable

class Group(Drawable):
    def __init__(self, x, y, width, height, config):
        """
           Initializes a group drawer.

           Args:
               x (float): the x position of the group
               y (float): the y position of the group
               width (float): the width of the group
               height (float): the height of the group
               config (Config): the drawing configuration of the group
        """
        super().__init__(x, y, width, height, config)
        self.children = []

    def add_child(self, drawable: Drawable):
        """
           Appends a drawable to this group's list of children.
        """
        self.children.append(drawable)