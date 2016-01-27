import json

class Shadow(object):

	@property
	def colour(self):
		return self._colour
	
	@colour.setter
	def colour(self, value):
		self._colour = value
	
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

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self.colour = data["_colour"]
		self.x = data["_x"]
		self.y = data["_y"]

	def __init__(self):
		self._colour = "black"
		self._x = 0
		self._y = 0

	def __str__(self):
		if (self._x > 0 or self._y > 0):
			return ": shadowcolor={0}: shadowx={1}: shadowy={2}".format(self._colour, self._x, self._y)
		return ""
