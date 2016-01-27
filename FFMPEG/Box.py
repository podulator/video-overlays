import json

class Box(object):

	@property
	def enabled(self):
		return self._enabled

	@enabled.setter
	def enabled(self, value):
		self._enabled =bool(value)

	@property
	def border_width(self):
		return self._border_width

	@border_width.setter
	def border_width(self, value):
		self._border_width = value

	@property
	def colour(self):
		return self._colour
	
	@colour.setter
	def colour(self, value):
		self._colour = value

	@property
	def opacity(self):
		return self._opacity
	
	@opacity.setter
	def opacity(self, value):
		self._opacity = value

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self.enabled = data["_enabled"]
		self.border_width = data["_border_width"]
		self.colour = data["_colour"]
		self.opacity = data["_opacity"]

	def __init__(self):
		self._enabled = False
		self._border_width = 0
		self._colour = "white"
		self._opacity = 1.0

	def __str__(self):
		if (self._enabled):
			return ": box=1: boxcolor={0}@{1}: boxborderw={2}".format(self._colour, self._opacity, self._border_width)
		return ""
