        
class Box:
            
    def __init__(self):
        self.enabled = 0
        self.border_width = 0
        self.colour = "white"
        self.opacity = 1.0

    def __str__(self):
        if (self.enabled):
            return ": box=1: boxcolor={0}@{1}: boxborderw={2}".format(self.colour, self.opacity, self.border_width)
        return ""