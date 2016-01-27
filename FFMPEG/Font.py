import json

class Font(object):

	@property
	def file(self):
		return self._file

	@file.setter
	def file(self, value):
		self._file = value
		self._family = None

	@property
	def family(self):
		return self._family

	@family.setter
	def family(self, value):
		self._family = value
		self._file = None

	@property
	def size(self):
		return self._size

	@size.setter
	def size(self, value):
		self._size = value
	
	@property
	def colour(self):
		return self._colour
	
	@colour.setter
	def colour(self, value):
		self._colour = value

	@property
	def alpha(self):
		return self._alpha
	
	@alpha.setter
	def alpha(self, value):
		self._alpha = value

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self.family = data["_family"]
		self.file = data["_file"]
		self.size = data["_size"]
		self.colour = data["_colour"]
		self.alpha = data["_alpha"]

	def __init__(self):
		self._family = "Sans"
		self._file = None
		self._size = 16
		self._colour = "black"
		self._alpha = 1.0

	def __str__(self):
		if (None == self._file):
			return ": font=\"{0}\": fontsize={1}: fontcolor={2}@{3}".format(self._family, self._size, self._colour, self._alpha)
		return ": fontfile=\"{0}\": fontsize={1}: fontcolor={2}@{3}".format(self._file, self._size, self._colour, self._alpha)
