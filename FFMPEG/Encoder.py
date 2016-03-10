import json

class MyFile(object):
	
	@property
	def name(self):
		return self._name
	
	@name.setter
	def name(self, value):
		self._name = value
		
	@property
	def flags(self):
		return self._flags
	
	@flags.setter
	def flags(self, value):
		self._flags = value

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self.name = data["_name"]
		self.flags = data["_flags"]
	
	def __init__(self, name = "", flags = ""):
		self.name = name
		self.flags = flags

class Encoder(object):
	
	@property
	def source(self):
		return self._source
	
	@property
	def destination(self):
		return self._destination
	
	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		if ("_source") in data:
			self._source.from_JSON(data["_source"])
		if ("_destination" in data):
			self._destination.from_JSON(data["_destination"])

	def __init__(self):
		self._source = MyFile()
		self._destination = MyFile()

	def __str__(self):
		return "{0} :: {1}".format(self._destination.name, self._destination.flags)

"""
class Encoder(object):

	@property
	def source_movie(self):
		return self._source_movie

	@source_movie.setter
	def source_movie(self, value):
		self._source_movie = value

	@property 
	def input_flags(self):
		return self._input_flags
	
	@input_flags.setter
	def input_flags(self, value):
		self._input_flags = value

	@property
	def extension(self):
		return self._extension
	
	@extension.setter
	def extension(self, value):
		self._extension = value
	
	@property
	def output_flags(self):
		return self._output_flags
	
	@output_flags.setter
	def output_flags(self, value):
		self._output_flags = value

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self.extension = data["_extension"]
		self._output_flags = data["_output_flags"]
		self.source_movie = data["_source_movie"]
		if ("_input_flags" in data):
			self._input_flags = data["_input_flags"]
		
	def __init__(self, source = "", extension = "", input_flags = "", output_flags = ""):
		self._source_movie = source
		self._extension = extension
		self._output_flags = output_flags
		self._input_flags = input_flags

	def __str__(self):
		return "{0} :: {1}".format(self._extension, self._output_flags)
"""
