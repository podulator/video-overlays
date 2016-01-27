from Renderable import Renderable
from Box import Box
from Font import Font
from Shadow import Shadow
import json
import re

class DrawImage(Renderable):

	def to_JSON(self):
		return json.dumps(self, default=lambda o: o.__dict__, sort_keys=True, indent=4)

	def from_JSON(self, data):
		pass

	def __init__(self, args):
		pass