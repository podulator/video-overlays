from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow
import json

class DrawText(Renderable):

    def render(self):
        
        border = ""
        if (self.border_width > 0):
            border = ": borderw={0}: bordercolor={1}".format(self.border_width, self.border_colour)
        
        bounds = ""
        if (self.fix_bounds):
            bounds = ": fix_bounds=1"

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
    def content(self):
        return self._content
    
    @content.setter
    def content(self, content):
        self._content = content

    @property
    def clean_content(self):
        return self._clean_content
    
    @clean_content.setter
    def clean_content(self, value):
        self._clean_content = bool(value)
    
    @property
    def content_max_length(self):
        return self._content_max_length
    
    @content_max_length.setter
    def content_max_length(self, length):
        self._content_max_length = length

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
    def y(self, y):
        self._y = y
    
    @property
    def alpha(self):
        return self._alpha

    @alpha.setter
    def alpha(self, alpha):
        self._alpha = alpha
        
    @property
    def border_width(self):
        return self._border_width
    
    @border_width.setter
    def border_width(self, width):
        self._border_width = width
        
    @property
    def border_colour(self):
        return self._border_colour
    
    @border_colour.setter
    def border_colour(self, colour):
        self._border_colour = colour
    
    @property
    def fix_bounds(self):
        return self._fix_bounds
    
    @fix_bounds.setter
    def fix_bounds(self, value):
        self._fix_bounds = value

    @property
    def font(self):
        return self._font
    
    @property
    def box(self):
        return self._box
    
    @property
    def drop_shadow(self):
        return self._shadow

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(self, text, frame_from, frame_to):
        
        Renderable.__init__(self, "drawtext", frame_from, frame_to)

        self._content = text
        self._clean_content = False
        self._content_max_length = 0
        
        # origin is top left
        self._x = 0
        self._y = 0
        self._alpha = 1.0
        self._border_width = 0
        self._border_colour = "black"
        self._fix_bounds = False;
        
        self._font = Font()
        self._box = Box()
        self._shadow = Shadow()

    def __str__(self):
        return self.render()
