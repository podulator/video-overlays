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
config.data_seperator = '|'
config.data_has_headers = True
config.max_rows = 5
config.terminate_on_completion = False
config.s3_destination = "video-transcodes-justgiving-com/my-story/%_PageShortName_%/"

template = config.to_JSON()
print (template)
