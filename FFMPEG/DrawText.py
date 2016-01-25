from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow

class DrawText(Renderable):

    def render(self):
        
        border = ""
        if (self.border_width > 0):
            border = ": borderw={0}: bordercolor={1}".format(self.border_width, self.border_colour)
        
        bounds = ""
        if (self.fix_bounds):
            bounds = ": fix_bounds=true"

        main = "text='{0}': x={1}: y={2}: alpha={3}{4}{5}".format(   
                                                                       self.content, 
                                                                       self.x, 
                                                                       self.y, 
                                                                       self.alpha, 
                                                                       border, 
                                                                       bounds)
    
        return "{0}=\"{1}{2}{3}{4}{5}\"".format(
                                        self.object_type, 
                                        main, 
                                        str(self._font), 
                                        str(self._shadow), 
                                        str(self._box), 
                                        self.enabled())

    @property
    def font(self):
        return self._font
    
    @property
    def box(self):
        return self._box
    
    @property
    def drop_shadow(self):
        return self._shadow

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
