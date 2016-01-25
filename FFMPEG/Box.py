        
class Box(object):

    @property
    def enabled(self):
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        self._enabled =bool(enabled)

    @property
    def border_width(self):
        return self._border_width

    @border_width.setter
    def border_width(self, width):
        self._border_width = width

    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, colour):
        self._colour = colour

    @property
    def opacity(self):
        return self._opacity
    
    @opacity.setter
    def opacity(self, opacity):
        self._opacity = opacity

    def __init__(self):
        self._enabled = False
        self._border_width = 0
        self._colour = "white"
        self._opacity = 1.0

    def __str__(self):
        if (self._enabled):
            return ": box=1: boxcolor={0}@{1}: boxborderw={2}".format(self._colour, self._opacity, self._border_width)
        return ""