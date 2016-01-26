from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow
from DrawText import DrawText
import json

class FFMPEG(object):

    FFMPEG_PATH = "/usr/bin/ffmpeg"

    def render(self):
        
        objects = join(" \\\n", self._text_objects)
        payload = "{0} -y i \"{1}\" \\\n-strict -2 \\\n-vf \\\n{2}{3}".format(FFMPEG_PATH, self._source_movie, objects, self._destination_movie)
        return payload

    def to_JSON(self):
        return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def __init__(source, destination):
        
        self._source_movie = source
        self._destination_movie = destination
        self._text_objects = []
        self._image_objects = []

    def __str__(self):
        return self.render()