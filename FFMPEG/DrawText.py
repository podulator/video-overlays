from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow
import json
import re
import textwrap
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup

class DrawText(Renderable):

	def fix_line_length(self):
		return '\n'.join(textwrap.wrap(self._content, self._line_max_length))

	def fix_content_length(self):
		return (self._content[:self._content_max_length - 3] + '...') if len(self._content) > self._content_max_length else self._content

	def scrub(self, content):
		content = BeautifulSoup(content).getText()
		content = unicode(BeautifulStoneSoup(content, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
		content = content.encode("utf-8")
		content = re.sub('%', '\\\\\\\\\\%', content)
		content = re.sub('{', '\\{', content)
		content = re.sub('}', '\\}', content)
		content = re.sub(':', '\\:', content)
		content = re.sub('!', '\\!', content)
		content = re.sub('\'', '', content)
		
		return content

	def render(self):

		if (self._content_dirty):
			if (self._clean_content):
				self._content = self.scrub(self._content)
				#print "content cleaned to {0}".format(self._content)
			if (self._content_max_length > 0 and self._content_max_length < len(self._content)):
				self._content = self.fix_content_length()
				#print "content shortened to {0} because longer than {1}".format(self._content, self._content_max_length)
			if (self._line_max_length > 0 and self._line_max_length < len(self._content)):
				self._content = self.fix_line_length()
				#print "content split to {0} because lines longer than {1}".format(self._content, self._line_max_length)

		self._content_dirty = False

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
										str(self.font), 
										str(self.drop_shadow), 
										str(self.box), 
										self.enabled())

	@property
	def content(self):
		'''
		if (self._content_dirty):
			if (self._clean_content):
				self._content = self.scrub(self._content)
				#print "content cleaned to {0}".format(self._content)
			if (self._content_max_length > 0 and self._content_max_length < len(self._content)):
				self._content = self.fix_content_length()
				#print "content shortened to {0} because longer than {1}".format(self._content, self._content_max_length)
			if (self._line_max_length > 0 and self._line_max_length < len(self._content)):
				self._content = self.fix_line_length()
				#print "content split to {0} because lines longer than {1}".format(self._content, self._line_max_length)

		self._content_dirty = False
		'''
		return self._content
	
	@content.setter
	def content(self, value):
		self._content_dirty = True
		self._content = value

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
	def content_max_length(self, value):
		self._content_max_length = value

	@property
	def line_max_length(self):
		return self._line_max_length
	
	@line_max_length.setter
	def line_max_length(self, value):
		self._line_max_length = value

	@property
	def x(self):
		return self._x
	
	@x.setter
	def x(self, value):
		self._x = value
	
	@property
	def y(self):
		return self._y
	
	@y.setter
	def y(self, value):
		self._y = value
	
	@property
	def alpha(self):
		return self._alpha

	@alpha.setter
	def alpha(self, value):
		self._alpha = value
		
	@property
	def border_width(self):
		return self._border_width
	
	@border_width.setter
	def border_width(self, value):
		self._border_width = value
		
	@property
	def border_colour(self):
		return self._border_colour
	
	@border_colour.setter
	def border_colour(self, value):
		self._border_colour = value
	
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
		return self._drop_shadow

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):

		self.content = data["_content"]
		self.clean_content = data["_clean_content"]
		self.content_max_length = data["_content_max_length"]
		self.line_max_length = data["_line_max_length"]

		self.frame_from = data["_frame_from"]
		self.frame_to = data["_frame_to"]
		
		self.x = data["_x"]
		self.y = data["_y"]
		self.alpha = data["_alpha"]
		self.border_width = data["_border_width"]
		self.border_colour = data["_border_colour"]
		self.fix_bounds = data["_fix_bounds"]

		self._box.from_JSON(data["_box"])
		self._font.from_JSON(data["_font"])
		self._drop_shadow.from_JSON(data["_drop_shadow"])

	def __init__(self, text = "", frame_from = 0, frame_to = 0):
		
		Renderable.__init__(self, "drawtext", frame_from, frame_to)

		self._content_dirty = False
		self.content = text
		self.clean_content = False
		self.content_max_length = 0
		self.line_max_length = 0

		# origin is top left
		self.x = 0
		self.y = 0
		self.alpha = 1.0
		self.border_width = 0
		self.border_colour = "black"
		self.fix_bounds = False;
		
		self._font = Font()
		self._box = Box()
		self._drop_shadow = Shadow()

	def __str__(self):
		return self.render()
