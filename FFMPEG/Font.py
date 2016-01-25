
class Font(object):

    @property
    def file(self):
        return self._file

    @file.setter
    def file(self, filename):
        self._file = filename
        self._family = None

    @property
    def family(self):
        return self._family

    @family.setter
    def family(self, family):
        self._family = family
        self._file = None

    @property
    def size(self):
        return self._size

    @size.setter
    def size(self, size):
        self._size = size
    
    @property
    def colour(self):
        return self._colour
    
    @colour.setter
    def colour(self, colour):
        self._colour = colour

    def __init__(self):
        self._family = "Sans"
        self._file = None
        self._size = 16
        self._colour = "black"

    def __str__(self):
        if (None == self._file):
            return ": font=\"{0}\": fontsize={1}: fontcolor={2}".format(self._family, self._size, self._colour)
        return ": fontfile=\"{0}\": fontsize={1}: fontcolor={2}".format(self._file, self._size, self._colour)
