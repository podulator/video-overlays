#!/usr/bin/python

# requires 
# urllib3, python-pip
# pip install boto BeautifulSoup

import csv
import boto.utils
import boto.ec2
from boto.s3.connection import S3Connection
import logging
import sys
import os
import json
import re
from socket import gethostname
import datetime
from FFMPEG import DrawText
from FFMPEG import FFMPEG
from Config import Config

s3_materials_path = ""
s3_logs_path = ""
cwd = os.getcwd()
CWD_TOKEN = "%_CWD_%"
local_materials = "{0}/materials".format(cwd)
tokenlist_file = "{0}/data.definition".format(local_materials)
template_file = "{0}/template.json".format(local_materials)
config_file = "{0}/config.json".format(local_materials)
log_file = "{}-{}.log".format( gethostname(), datetime.datetime.now().isoformat(' ') )
log_file = log_file.replace(" ", "-")
    
def setDebugLevel(val):
	logger.setLevel(val)
	log_console.setLevel(val)
	log_file_handler.setLevel(val)

def show_help():
	path = sys.argv[0]
	print "run as {0} [ -help or -local or S3MaterialsURL or S3MaterialsURL:S3LogsURL ]".format(path)
	print "-help :: show this help"
	print "-local :: assume all materials alreaady exist under ./materials/"
	print "S3MaterialsURL :: The full bucket name and path to a materials forlder. Logs will be stored in derived bucketname/video_logs"
	print "S3MaterialsURL:S3LogsURL :: Full bucket name and path for both materials and logs, colon seperated"
	print ""

def get_bucket_and_path_from_s3_url(url):
	url_parts = url.split("/")
	# get the path minus the bucket name
	bucket = url_parts[0]
	path_root = "/".join(url_parts[1:])
	# always force a trailing slash if it's not an empty string
	if ("" != path_root):
		if ("/" != path_root[-1]):
			path_root = "{0}/".format(path_root)
			logger.debug("Path normalised to :: {0}".format(path_root))
	
	logger.debug("Bucket == {0} :: Path = {1}".format(bucket, path_root))
	return bucket, path_root

def upload_file_to_S3(source, destination):
	try:
		logger.info("Uploading {0} to {1}".format(source, destination))
		bucket_name, path = get_bucket_and_path_from_s3_url(destination)
		# strip trailing slash
		path = path[:-1]
		logger.debug("Connecting to bucket :: {}".format(bucket_name))
		conn = S3Connection()
		bucket = conn.get_bucket(bucket_name)
		logger.debug("Setting key :: {0}".format(path))
		key = boto.s3.key.Key(bucket)
		key.key = path
		key.set_contents_from_filename(source)
		logger.info("Upload complete")
		return True
	except Exception as e:
		logger.error(e)
		return False

# sort out the start up params from the cli or fall back to user data
def handle_startup_params():
	global s3_materials_path, s3_logs_path
	params = ""
	if (len(sys.argv) > 1):
		params = sys.argv[1]
		logger.debug("Got startup params :: {0}".format(params))
	else:
		logger.info("Trying to get startup params from user data")
		params = boto.utils.get_instance_userdata()
	
	params = params.strip()
	if (len(params) == 0):
		show_help()
		exit(1)
	else:
		if (params == "-help"):
			show_help()
			exit(0)
		elif (params == "-local"):
			pass
		else:
			param_parts = params.split(":")
			if (len(param_parts) >= 2):
				s3_materials_path = param_parts[0]
				s3_logs_path = param_parts[1]
			else:
				s3_materials_path = param_parts[0]
				s3_logs_bucket, discard_path = get_bucket_and_path_from_s3_url(s3_materials_path)
				s3_logs_path = "{0}/video_logs/".format(s3_logs_bucket)
	logger.debug("s3_materials_path = {0}".format(s3_materials_path))
	logger.debug("s3_logs_path = {0}".format(s3_logs_path))

def LoadTokenList(data_file):
	global data_seperator
	with open(data_file, 'rb') as f:
		reader = csv.reader(f, quotechar='"', delimiter=str(data_seperator), quoting=csv.QUOTE_ALL, skipinitialspace=True)
		for row in reader:
			# add the cwd token
			row.append(CWD_TOKEN)
			logger.debug("data definitions :: {0}".format( " :: ".join( map( str, row ) ) ) )
			return row

def CsvDataIterator(data_file):
	global data_seperator
	with open(data_file, 'rb') as f:
		reader = csv.reader(f, quotechar='"', delimiter=str(data_seperator), quoting=csv.QUOTE_NONE, skipinitialspace=True)
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

# logging setup

if (os.path.exists("*.log")):
	os.remove("*.log")

logger = logging.getLogger('Video Processor')
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
log_console = logging.StreamHandler(sys.stdout)
log_console.setFormatter(formatter)
logger.addHandler(log_console)

log_file_handler = logging.FileHandler(log_file)
log_file_handler.setFormatter(formatter)
logger.addHandler(log_file_handler)

setDebugLevel(logging.INFO)

# end logging setup

logger.info("Run started")

'''
fetch materials?
'''

try:

	handle_startup_params()

	if not os.path.exists(local_materials):
		os.mkdir(local_materials)

	if (len(s3_materials_path) > 0):
		
		remote_bucket, remote_path_root = get_bucket_and_path_from_s3_url(s3_materials_path)
		remote_path_root_length = len(remote_path_root)

		logger.info("Downloading materials from bucket :: {0}".format(remote_bucket))
		s3_conn = boto.connect_s3()
		bucket = s3_conn.get_bucket(remote_bucket)
		bucket_list = bucket.list(remote_path_root)
		for item in bucket_list:
			remote_key = str(item.key)
			local_path = "{0}/{1}".format(local_materials, remote_key[remote_path_root_length:])
			logger.info("Downloading {0} to {1}".format(remote_key, local_path))
			try:
				#item.get_contents_to_filename(local_path)
				pass
			except OSError:
				if not os.path.exists(local_path):
					logger.info("Creating local folder :: {0}".format(local_path))
					os.mkdir(local_path)
		logger.info("All materials downloaded")

	else:
		logger.info("No materials bucket supplied, assuming everything is already local")
		
except ValueError as e:
	logger.error("Couldn't fetch materials :: {0}".format(e))
	exit(1)

'''
config loading starts
'''

config = Config()
logger.info("Loading json config from {0}".format(config_file))
with open(config_file, 'r') as myfile:
	config.from_JSON(json.loads(myfile.read().strip()))
logger.info("Loaded json config")
skip_headers = config.data_has_headers
data_seperator = config.data_seperator
max_rows = config.max_rows
data_file = "{0}/{1}".format(local_materials, config.data_file)

logger.info("Loading json template from {0}".format(template_file))
with open(template_file, 'r') as myfile:
	template = json.loads(myfile.read().strip())
logger.info("Loaded json template")

logger.info("Loading token list from {0}".format(tokenlist_file))
tokens = LoadTokenList(tokenlist_file)
logger.info("Loaded {0} tokens".format( len( tokens ) ) )

'''
config loading ends
'''

# start processing
if (skip_headers and (max_rows > 0)):
	max_rows += 1

for row_counter, data_row in enumerate(CsvDataIterator(data_file)):
    if (len(data_row) > 0):
		if (0 == row_counter):
			if (len(data_row) != len(tokens)):
				logger.error("Data definition doesn't match row data")
				raise ValueError("Data definition doesn't match row data")
			if (skip_headers):
				continue
		if (max_rows > 0 and max_rows <= row_counter):
			break
		logger.info("processing row :: {0}".format(row_counter))

		# load the template as json
		this_script = FFMPEG()
		this_script.from_JSON(template)
		
		if (config.create_movie):
			logger.info("Creating movies of type :: {0}".format(", ".join( map( str, (this_script.output_encoders) ) ) ) )
				
			# fix input output paths possibly containing tokens
			this_script.source_movie = swap_tokens(tokens, data_row, this_script.source_movie)
			this_script.destination_movie = swap_tokens(tokens, data_row, this_script.destination_movie)
			this_script.snapshot_name = swap_tokens(tokens, data_row, this_script.snapshot_name)

			# swap tokens for data in the template
			for text_object in this_script.text_objects:
				text_object.font.file = re.sub(CWD_TOKEN, cwd, text_object.font.file)
				text_object.content = swap_tokens(tokens, data_row, text_object.content)

			# run the command
			# this_script.render_movies()
			print ",\n\n".join( map( str, this_script.render_movies() ) )

			# do a snapshot?
			if (config.create_snapshot):
				logger.info("Creating snapshot")
				print this_script.render_snapshot()

		if (config.create_html):
			logger.info("Creating html")

logger.info("Run completed")
upload_file_to_S3(log_file, "{0}/{1}".format(s3_logs_path, log_file))
