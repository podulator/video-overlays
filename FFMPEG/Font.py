
class Font:

    def __init__(self):
        self.family = "Sans"
        self.file = None
        self.size = 16
        self.colour = "black"

    def __str__(self):
        return ": font={0}: fontfile={1}: fontsize={2}: fontcolor={3}".format(self.family, self.file, self.size, self.colour)