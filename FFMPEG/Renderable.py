
class Renderable(object):
    """The basic FFMPEG drawable class"""

    def object_type(self):
        return self.object_type

    def enabled(self):
        return ": enable='gt(n,{0})*lt(n,{1})'".format(str(self.frame_from), str(self.frame_to))
    
    def __init__(self, object_type, frame_from, frame_to):
        self.object_type = object_type
        self.frame_from = frame_from
        self.frame_to = frame_to

    def __str__(self):
        return  "{0}=\"{1}\"".format(self.object_type, self.enabled())