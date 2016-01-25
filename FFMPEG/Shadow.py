
class Shadow(object):

    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, colour):
        self._colour = colour
    
    @property
    def x(self):
        return self._x
    
    @x.setter
    def x(self, x):
        self._x = x
    
    @property
    def y(self):
        return self._y
    
    @y.setter
    def set_y(self, y):
        self._y = y

    def __init__(self):
        self._colour = "black"
        self._x = 0
        self._y = 0

    def __str__(self):
        if (self._x > 0 or self._y > 0):
            return ": shadowcolor={0}: shadowx={1}: shadowy={2}".format(self._colour, self._x, self._y)
        return ""
