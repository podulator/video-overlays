from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow
from DrawText import DrawText
from DrawImage import DrawImage
from Encoder import Encoder
import json

class FFMPEG(object):

	FFMPEG_PATH = "/usr/bin/ffmpeg"

	@property
	def output_path_prefix(self):
		return self._output_path_prefix
	
	@output_path_prefix.setter
	def output_path_prefix(self, value):
		self._output_path_prefix = value

	@property 
	def input_flags(self):
		return self._input_flags
	
	@input_flags.setter
	def input_flags(self, value):
		self._input_flags = value

	@property
	def destination_movie(self):
		return self._destination_movie

	@destination_movie.setter
	def destination_movie(self, value):
		self._destination_movie = value

	@property
	def snapshot_timestamp(self):
		return self._snapshot_timestamp
	
	@snapshot_timestamp.setter
	def snapshot_timestamp(self, value):
		self._snapshot_timestamp = value

	@property
	def snapshot_name(self):
		return self._snapshot_name
	
	@snapshot_name.setter
	def snapshot_name(self, value):
		self._snapshot_name = value

	@property
	def text_objects(self):
		return self._text_objects
	
	@property
	def image_objects(self):
		return self._image_objects

	@property
	def output_encoders(self):
		return self._output_encoders

	def render_movies(self):

		results = []

		# make the filters up
		filter_objects = self._text_objects + self._image_objects
		filter_objects = ",\\\n".join( map( str, self._text_objects ) )
		filters = "-vf \\\n{0} \\\n".format(filter_objects)
		
		for encoder in self._output_encoders:
			inputs = "{0} -y -i \"{1}\" {2} \\\n".format(self.FFMPEG_PATH, encoder._source_movie, self._input_flags)
			movie_name = "{}.{}".format(self._destination_movie, encoder.extension)
			outputs = "{0} \"{1}/{2}\"".format(encoder.flags, self._output_path_prefix, movie_name)
			payload = "{0}{1}{2}".format(inputs, filters, outputs)
			results.append([movie_name, payload])

		return results

	def render_snapshot(self):
		if (self.snapshot_name != "" and self.snapshot_timestamp != ""):
			# just take the first rendered movie as an input, no matter how many there are
			for encoder in self._output_encoders:
				src_movie = "{0}.{1}".format(self._destination_movie, encoder.extension)
				snapshot = "{0} -y -i \"{1}/{2}\" -ss {3} -vframes 1 {4}/{5}".format(self.FFMPEG_PATH, self._output_path_prefix, src_movie, self.snapshot_timestamp, self._output_path_prefix, self.snapshot_name)
				return [self._snapshot_name, snapshot]
		return ""

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		
		if ("_destination_movie" in data):
			self.destination_movie = data["_destination_movie"]
		
		if ("_snapshot_timestamp" in data):
			self.snapshot_timestamp = data["_snapshot_timestamp"]
		
		if ("_snapshot_name" in data):
			self._snapshot_name = data["_snapshot_name"]
		
		if ("_input_flags" in data):
			self._input_flags = data["_input_flags"]
		
		if ("_output_path_prefix" in data):
			self._output_path_prefix = data["_output_path_prefix"]

		if ("_text_objects" in data):
			for text_object in data["_text_objects"]:
				drawtext = DrawText()
				drawtext.from_JSON(text_object)
				self._text_objects.append(drawtext)
		
		if ("_image_objects" in data):
			for image_object in data["_image_objects"]:
				image = DrawImage()
				image.from_JSON(image_object)
				self._image_objects.append(image)

		if ("_output_encoders" in data):
			for encoder_object in data["_output_encoders"]:
				encoder = Encoder()
				encoder.from_JSON(encoder_object)
				self._output_encoders.append(encoder)

	def __init__(self, destination = ""):

		self._destination_movie = destination
		self._snapshot_timestamp = ""
		self._snapshot_name = ""
		self._input_flags = ""
		self._output_path_prefix = ""

		self._text_objects = []
		self._image_objects = []
		self._output_encoders = []

	def __str__(self):
		return ",\n\n".join( map( str, self.render_movies() ) )
