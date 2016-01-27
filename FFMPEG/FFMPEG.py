from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow
from DrawText import DrawText
from DrawImage import DrawImage
import json

class FFMPEG(object):

	FFMPEG_PATH = "/usr/bin/ffmpeg"

	@property
	def source_movie(self):
		return self._source_movie

	@source_movie.setter
	def source_movie(self, value):
		self._source_movie = value

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

	def render(self):
		
		all_objects = self._text_objects + self._image_objects
		all_objects = ",\\\n".join( map( str, self._text_objects ) )
		payload = "{0} -y -i \"{1}\" \\\n-strict -2 \\\n-vf \\\n{2} \\\n\"{3}\"".format(self.FFMPEG_PATH, self._source_movie, all_objects, self._destination_movie)
		
		if (self.snapshot_name != "" and self.snapshot_timestamp != ""):
			snapshot = "\n{0} -y -i {1} -ss {2} -vframes 1 {3}".format(self.FFMPEG_PATH, self._destination_movie, self.snapshot_timestamp, self.snapshot_name)
			payload += snapshot

		return payload

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):

		self.source_movie = data["_source_movie"]
		self.destination_movie = data["_destination_movie"]
		self.snapshot_timestamp = data["_snapshot_timestamp"]
		self._snapshot_name = data["_snapshot_name"]

		for text_object in data["_text_objects"]:
			drawtext = DrawText()
			drawtext.from_JSON(text_object)
			self._text_objects.append(drawtext)
		for image_object in data["_image_objects"]:
			image = DrawImage()
			image.from_JSON(image_object)
			self._image_objects.append(image)

	def __init__(self, source = "", destination = ""):
		
		self._source_movie = source
		self._destination_movie = destination
		self._snapshot_timestamp = ""
		self._snapshot_name = ""

		self._text_objects = []
		self._image_objects = []

	def __str__(self):
		return self.render()
