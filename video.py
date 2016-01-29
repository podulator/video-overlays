#!/usr/bin/python

# requires 
# urllib3, python-pip
# pip install boto BeautifulSoup

import csv
from boto.s3.connection import S3Connection
import logging
import sys
import os
import json
import re
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
        reader = csv.reader(f, quotechar='"', delimiter='|', quoting=csv.QUOTE_NONE, skipinitialspace=True)
        for row in reader:
			# add the cwd token
			row.append(CWD_TOKEN)
			logger.debug("data definitions :: {0}".format( " :: ".join( map( str, row ) ) ) )
			return row

def CsvDataIterator(data_file):
	with open(data_file, 'rb') as f:
		reader = csv.reader(f, quotechar='"', delimiter='|', quoting=csv.QUOTE_NONE, skipinitialspace=True)
		for row in reader:
			# add the cwd value
			row.append(cwd)
			yield row

def swap_tokens(tokens, data_row, content):

	for token_counter, token in enumerate(tokens):
		data = data_row[token_counter]

		if (re.match(token, content)):
			logger.debug("swapping out token :: {0} for data :: '{1}'".format(token, data))
			content = re.sub(token, data, content)

	return content

data_file = 'sample.csv'
tokenlist_file = 'data.definition'
template_file = 'template.json.bak'
skip_headers = True
max_rows = 5
cwd = os.getcwd()
CWD_TOKEN = "%_CWD_%"

logger.info("Loading json template from {0}".format(template_file))
with open(template_file, 'r') as myfile:
	template = json.loads(myfile.read().strip())
logger.info("Loaded json template")

logger.info("Loading token list from {0}".format(tokenlist_file))
tokens = LoadTokenList(tokenlist_file)
logger.info("Loaded {0} tokens".format( len( tokens ) ) )

# start processing
if (skip_headers and (max_rows > 0)):
	max_rows += 1

for row_counter, data_row in enumerate(CsvDataIterator(data_file)):
    if (len(data_row) > 0):
		if (skip_headers and (0 == row_counter)):
		  continue
		if (max_rows > 0 and max_rows <= row_counter):
			break
		logger.info("processing row :: {0}".format(row_counter))

		# load the template as json
		this_script = FFMPEG()
		this_script.from_JSON(template)
		
		# fix input output paths possibly containing tokens
		this_script.source_movie = swap_tokens(tokens, data_row, this_script.source_movie)
		this_script.destination_movie = swap_tokens(tokens, data_row, this_script.destination_movie)
		this_script.snapshot_name = swap_tokens(tokens, data_row, this_script.snapshot_name)

		# swap tokens for data in the template
		for text_object in this_script.text_objects:
			text_object.font.file = re.sub(CWD_TOKEN, cwd, text_object.font.file)
			#print text_object.content
			text_object.content = swap_tokens(tokens, data_row, text_object.content)

		print this_script

