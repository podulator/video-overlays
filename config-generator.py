#!/usr/bin/python

# requires 
# urllib3, python-pip
# pip install boto BeautifulSoup

import sys
import os

from Config import Config

config = Config()
config.create_html = True
config.create_movie = True
config.create_snapshot = True
config.data_file = "sample.csv"
config.data_definition_file = "data.definition"
config.data_seperator = '|'
config.data_has_headers = True
config.html_output_file = "index.html"
config.html_template = "template.html"
config.s3_materials = "video-transcodes-justgiving-com/config/materials"
config.max_rows = 1
config.terminate_on_completion = False
config.s3_destination = "video-transcodes-justgiving-com/my-story/%_PageShortName_%/"
config.script_file = "template.json"

template = config.to_JSON()
print (template)

