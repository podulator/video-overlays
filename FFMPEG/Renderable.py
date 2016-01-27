
class Renderable(object):
	"""The basic FFMPEG drawable class"""

	@property
	def object_type(self):
		return self._object_type

	@object_type.setter
	def object_type(self, value):
		self._data_type = value
	
	@property
	def frame_from(self):
		return self._frame_from
	
	@frame_from.setter
	def frame_from(self, value):
		self._frame_from = value
	
	@property
	def frame_to(self):
		return self._frame_to
	
	@frame_to.setter
	def frame_to(self, value):
		self._frame_to = value

	def enabled(self):
		return ": enable='gt(n,{0})*lt(n,{1})'".format(str(self.frame_from), str(self.frame_to))
	
	def __init__(self, object_type, frame_from, frame_to):
		self._object_type = object_type
		self._frame_from = frame_from
		self._frame_to = frame_to

	def __str__(self):
		return  "{0}=\"{1}\"".format(self.object_type, self.enabled())