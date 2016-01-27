#!/usr/bin/python

# requires 
# urllib3, python-pip
# pip install boto BeautifulSoup

import csv
from boto.s3.connection import S3Connection
import logging
import sys
import os

from FFMPEG import DrawText
from FFMPEG import FFMPEG

# logging setup

logger = logging.getLogger('Video Processor')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
logger.addHandler(ch)

def setDebugLevel(val):
    logger.setLevel(val)
    ch.setLevel(val)

debugLevel = logging.INFO
debugLevel = logging.DEBUG
setDebugLevel(debugLevel)

# end logging setup

def LoadTokenList(data_file):
    with open(data_file, 'rb') as f:
        rows = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        tokens = rows.next()
        logger.debug("data definitions :: {0}".format( " :: ".join( map( str, tokens ) ) ) )
        return tokens

def CsvDataIterator(data_file):
    with open(data_file, 'rb') as f:
        reader = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
        for row in reader:
            yield row

'''
tokenlist_file = 'data.definition'
logger.info("Loading token list from {0}".format(tokenlist_file))
tokens = LoadTokenList(tokenlist_file)
logger.info("Loaded {0} tokens".format( len( tokens ) ) )
'''

'''
movie = FFMPEG("Just Giving 008 Animatic.mov", "outmovie.webm")

text_object = DrawText("demo text that is getting quite long now and wraps at 30 chars", 100, 500)
text_object.line_max_length = 30
text_object.fix_bounds = True
text_object.font.file = "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-C.ttf"
text_object.font.size = 80
text_object.box.enabled = False
text_object.box.colour = "0000AA99"
text_object.box.border_width = 30
text_object.x = 200
text_object.y = 700

text_object2 = DrawText('second [escaped] {demo} %text% that is getting quite long :: now and needs more of a test', 300, 600)
text_object2.line_max_length = 20
text_object2.fix_bounds = True
text_object2.font.file = "/usr/share/fonts/truetype/ubuntu-font-family/Ubuntu-C.ttf"
text_object2.font.size = 80
text_object2.box.enabled = False
text_object2.box.colour = "FF00AA00"
text_object2.box.border_width = 30
text_object2.clean_content = True
text_object2.x = 600
text_object2.y = 100

movie.text_objects.append(text_object)
movie.text_objects.append(text_object2)

print (movie)

'''

import json
with open('template.json', 'r') as myfile:
	template = json.loads(myfile.read())
	movie = FFMPEG()
	movie.from_JSON(template)
	print movie


#data_file = 'PageReportV2.csv'
#for row in CsvDataIterator(data_file):
#    row[4] = HTMLEntitiesToUnicode(BeautifulSoup(row[4]).getText())
    #logger.debug(row)

