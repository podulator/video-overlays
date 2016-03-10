import json

class Encoder(object):

	@property
	def source_movie(self):
		return self._source_movie

	@source_movie.setter
	def source_movie(self, value):
		self._source_movie = value

	@property
	def extension(self):
		return self._extension
	
	@extension.setter
	def extension(self, value):
		self._extension = value
	
	@property
	def flags(self):
		return self._flags
	
	@flags.setter
	def flags(self, value):
		self._flags = value

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self.extension = data["_extension"]
		self._flags = data["_flags"]
		self.source_movie = data["_source_movie"]
			
	def __init__(self, source = "", extension = "", flags = ""):
		self._source_movie = source
		self._extension = extension
		self._flags = flags

	def __str__(self):
		return "{0} :: {1}".format(self._extension, self._flags)
