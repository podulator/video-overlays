import json

class Config(object):

	@property
	def create_html(self):
		return self._create_html
	
	@create_html.setter
	def create_html(self, value):
		self._create_html = value
		
	@property
	def create_movie(self):
		return self._create_movie
	
	@create_movie.setter
	def create_movie(self, value):
		self._create_movie = value

	@property
	def create_snapshot(self):
		return self._create_snapshot
	
	@create_snapshot.setter
	def create_snapshot(self, value):
		self._create_snapshot = value

	@property
	def data_file(self):
		return self._data_file
	
	@data_file.setter
	def data_file(self, value):
		self._data_file = value

	@property
	def data_has_headers(self):
		return self._data_has_headers
	
	@data_has_headers.setter
	def data_has_headers(self, value):
		self._data_has_headers = value

	@property
	def data_seperator(self):
		return self._data_seperator
	
	@data_seperator.setter
	def data_seperator(self, value):
		self._data_seperator = value

	@property
	def max_rows(self):
		return self._max_rows
	
	@max_rows.setter
	def max_rows(self, value):
		self._max_rows = value

	@property
	def s3_destination(self):
		return self._s3_destination
	
	@s3_destination.setter
	def s3_destination(self, value):
		self._s3_destination = value

	@property
	def terminate_on_completion(self):
		return self._terminate_on_completion
	
	@terminate_on_completion.setter
	def terminate_on_completion(self, value):
		self._terminate_on_completion = value

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		self._create_html = data["_create_html"]
		self._create_movie = data["_create_movie"]
		self._create_snapshot = data["_create_snapshot"]
		self._data_file = data["_data_file"]
		self._data_seperator = data["_data_seperator"]
		self._data_has_headers = data["_data_has_headers"]
		self._max_rows = data["_max_rows"]
		self._s3_destination = data["_s3_destination"]
		self._terminate_on_completion = data["_terminate_on_completion"]

	def __init__(self):
		self._create_html = True
		self._create_movie = True
		self._create_snapshot = True
		self._data_file = ""
		self._data_seperator = ","
		self._data_has_headers = False
		self._max_rows = 0
		self._s3_destination = ""
		self._terminate_on_completion = False


