
class Shadow:

    def __init__(self):
        self.colour = "black"
        self.x = 0
        self.y = 0
    
    def __str__(self):
        if (self.x > 0 or self.y > 0):
            return ": shadowcolor={0}: shadowx={1}: shadowy={2}".format(self.colour, self.x, self.y)
        return ""