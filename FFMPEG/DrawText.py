from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow

class DrawText(Renderable):

    def render(self):
        return "{0}=\"text={1}: x={2}: y={3}: alpha={4}{5}{6}{7}{8}\"".format(self.object_type, 
                                                                       self.content, 
                                                                       self.x, 
                                                                       self.y, 
                                                                       self.alpha, 
                                                                       str(self._font), 
                                                                       str(self._shadow), 
                                                                       str(self._box), 
                                                                       self.enabled())

    def __init__(self, text, frame_from, frame_to):
        
        Renderable.__init__(self, "drawtext", frame_from, frame_to)

        self.content = text
        # origin is top left
        self.x = 0
        self.y = 0
        self.alpha = 1.0
        self.border_width = 0
        self.border_colour = "black"
        self.fix_bounds = False;
        
        self._font = Font()
        self._box = Box()
        self._shadow = Shadow()

    def __str__(self):
        return self.render()
