#!/usr/bin/python
# -*- coding: utf-8 -*-

# requires 
# apt-get install ffmpeg python python-urllib3, python-pip
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
import ssl
import traceback

# workaround buckets with periods in their name
if hasattr(ssl, '_create_unverified_context'):
   ssl._create_default_https_context = ssl._create_unverified_context

s3_config_path = ""
cwd = os.getcwd()
CWD_TOKEN = "%_CWD_%"
local_materials = "{0}/materials".format(cwd)
local_output = "{0}/outputs".format(cwd)
config_file = "{0}/config.json".format(cwd)
log_file = "{}-{}.log".format( gethostname(), datetime.datetime.now().isoformat(' ') )
log_file = log_file.replace(" ", "-")
running_locally = False
running_on_ec2 = False
instance_id = ""

def setDebugLevel(val):
	logger.setLevel(val)
	log_console.setLevel(val)
	log_file_handler.setLevel(val)

def show_help():
	path = sys.argv[0]
	print "run as {0} [ -help or -local or S3ConfigFileUrl ]".format(path)
	print "-help :: show this help"
	print "-local :: assume all materials alreaady exist under {0}/materials/".format(cwd)
	print "S3ConfigFileUrl :: The full bucket name and path to a valid config file. Logs will be stored in materials bucketname/video_render_logs"
	print ""

def purge(dir, pattern):
	for f in os.listdir(dir):
		if re.search(pattern, f):
			os.remove(os.path.join(dir, f))

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

def upload_file_to_S3(source, destination, make_public = False):
	try:
		logger.debug("Uploading {0} to {1}".format(source, destination))
		bucket_name, path = get_bucket_and_path_from_s3_url(destination)
		# strip trailing slash
		path = path[:-1]
		logger.debug("Connecting to bucket :: {}".format(bucket_name))
		
		conn = S3Connection()
		bucket = conn.get_bucket(bucket_name)
		logger.debug("Setting key :: {0}".format(path))
		key = boto.s3.key.Key(bucket)
		key.key = path
		# do the upload
		key.set_contents_from_filename(source)
		# make it public?
		if (make_public):
			key.set_acl('public-read')
		logger.debug("Upload complete")
		return True
	except Exception as e:
		logger.error(e)
		return False

# sort out the start up params from the cli or fall back to user data
def handle_startup_params():
	global s3_config_path, running_locally, running_on_ec2, instance_id
	params = ""
	if (len(sys.argv) > 1):
		params = sys.argv[1]
		logger.debug("Got startup params :: {0}".format(params))
	else:
		logger.info("Trying to get startup params from user data")
		params = boto.utils.get_instance_userdata()
		instance_id = boto.utils.get_instance_metadata()['instance-id']
		if (len(instance_id) > 0):
			running_on_ec2 = True
			logger.info("Running on instance id :: {0}".format(instance_id))
			logger.info("Got user_data params :: {0}".format(params))
	params = params.strip()
	if (len(params) == 0):
		show_help()
		exit(1)
	else:
		if (params == "-help"):
			show_help()
			exit(0)
		elif (params == "-local"):
			running_locally = True
		else:
			s3_config_path = params

	logger.debug("s3_config_path = {0}".format(s3_config_path))

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
	try:
		logger.debug("Looking for tokens in :: {0}".format(content))
	except UnicodeEncodeError:
		logger.debug(u"Looking for tokens in :: {0}".format(content))
	for token_counter, token in enumerate(tokens):
		if (None != re.search(token, content)):
			data = data_row[token_counter].decode("utf8", "ignore")
			try:
				logger.debug("swapping out token :: {0} for data :: '{1}'".format(token, data))
			except UnicodeEncodeError:
				logger.debug(u"swapping out token :: {0} for data :: '{1}'".format(token, data))
			#content = content.replace(token, data)
			content = re.sub(token, data, content)

	return content

def swap_tokens_html(tokens, data_row, content):
	try:
		logger.debug("Looking for tokens in :: {0}".format(content))
	except UnicodeEncodeError:
		logger.debug(u"Looking for tokens in :: {0}".format(content))
	for token_counter, token in enumerate(tokens):
		if (None != re.search(token, content)):
			data = data_row[token_counter]
			try:
				logger.debug("swapping out token :: {0} for data :: '{1}'".format(token, data))
			except UnicodeEncodeError:
				logger.debug(u"swapping out token :: {0} for data :: '{1}'".format(token, data))
			#content = content.replace(token, data)
			content = re.sub(token, data, content)

	return content

# logging setup

purge(cwd, ".log$")
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

	if (not os.path.exists(local_materials)):
		os.mkdir(local_materials)
	if (not os.path.exists(local_output)):
		os.mkdir(local_output)

	if (len(s3_config_path) > 0):

		# download the config file
		config_bucket, config_key = get_bucket_and_path_from_s3_url(s3_config_path)
		# strip trailing slash as this is a file, not a dir
		config_key = config_key[:-1]
		logger.info("Downloading config from bucket :: {0}".format(config_bucket))
		s3_conn = boto.connect_s3()
		
		bucket = s3_conn.get_bucket(config_bucket)
		key = bucket.get_key(config_key)
		logger.info("Downloading config file {0} to {1}".format(config_key, config_file))
		key.get_contents_to_filename(config_file)

	# by now we should always have a local or a downloaded config file
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
	data_defintion_file = "{0}/{1}".format(local_materials, config.data_definition_file)
	template_file = "{0}/{1}".format(local_materials, config.script_file)

	# get s3 materials if they're specified and we're not running locally
	if (len(config.s3_materials) > 0 and not running_locally):

		remote_bucket, remote_path_root = get_bucket_and_path_from_s3_url(config.s3_materials)
		remote_path_root_length = len(remote_path_root)

		logger.info("Downloading materials from bucket :: {0}".format(remote_bucket))
		s3_conn = boto.connect_s3()
		bucket = s3_conn.get_bucket(remote_bucket)
		bucket_list = bucket.list(remote_path_root)
		for item in bucket_list:
			remote_key = str(item.key)
			local_path = "{0}/{1}".format(local_materials, remote_key[remote_path_root_length:])
			if (not os.path.isfile(local_path)):
				logger.info("Downloading {0} to {1}".format(remote_key, local_path))
				try:
					item.get_contents_to_filename(local_path)
				except OSError:
					if not os.path.exists(local_path):
						logger.info("Creating local folder :: {0}".format(local_path))
						os.mkdir(local_path)
			else:
				logger.info("Skipping existing file :: {0}".format(local_path))

		logger.info("All materials downloaded")

	else:
		logger.info("No materials bucket supplied, assuming everything is already local")
		
except ValueError as e:
	logger.error("Couldn't fetch materials :: {0}".format(e))
	exit(1)

logger.info("Loading json template from {0}".format(template_file))
with open(template_file, 'r') as myfile:
	template = json.loads(myfile.read().strip())
logger.info("Loaded json template")

logger.info("Loading token list from {0}".format(data_defintion_file))
tokens = LoadTokenList(data_defintion_file)
logger.info("Loaded {0} tokens".format( len( tokens ) ) )

if (config.create_html):
	html_template_path = "{0}/{1}".format(local_materials, config.html_template)
	if (os.path.exists(html_template_path)):
		logger.info("Loading html template from {0}".format(html_template_path))
		with open(html_template_path, 'r') as f:
			html_template = f.read().strip()
		logger.info("Loaded html template")

	iframe_template_path =  "{0}/{1}".format(local_materials, config.iframe_template)
	if (os.path.exists(iframe_template_path)):
		logger.info("Loading iframe template from {0}".format(iframe_template_path))
		with open(iframe_template_path, 'r') as f:
			iframe_template = f.read().strip()
		logger.info("Loaded iframe template")
'''
config loading ends
'''

# start processing
if (skip_headers and (max_rows > 0)):
	max_rows += 1

for row_counter, data_row in enumerate(CsvDataIterator(data_file)):
	if (len(data_row) == 0):
		continue
	if (len(data_row) != len(tokens)):
		logger.error("Data definition doesn't match row data for row :: {0}".format(row_counter))
		continue

	try:
		# headers and limits checking
		if (0 == row_counter and skip_headers):
			continue
		if (max_rows > 0 and max_rows <= row_counter):
			break

		logger.info("processing row :: {0}".format(row_counter))

		if (config.create_movie):

			# load the template as json
			this_script = FFMPEG()
			this_script.from_JSON(template)
			this_script.output_path_prefix = local_output
			
			# we need to work out paths and filenames  for html even if we don't render the movie
			logger.debug("Creating movies of type :: {0}".format(", ".join( map( str, (this_script.encoders) ) ) ) )

			# fix input output paths possibly containing tokens
			for encoder in this_script.encoders:
				encoder.source.name = swap_tokens(tokens, data_row, encoder.source.name)
				encoder.destination.name = swap_tokens(tokens, data_row, encoder.destination.name)

			this_script.snapshot_name = swap_tokens(tokens, data_row, this_script.snapshot_name)

			# swap tokens for data in the template
			for text_object in this_script.text_objects:
				text_object.font.file = re.sub(CWD_TOKEN, cwd, text_object.font.file)
				text_object.content = swap_tokens(tokens, data_row, text_object.content)

			movies = this_script.render_movies()

			# run the command
			logger.info("Rendering {0} movies".format(len(movies)))
			for movie in movies:

				movie_name = movie[0]
				movie_script = movie[1]
				
				logger.info("Rendering :: {0}".format(movie_name))

				# actually execute the command
				result = os.system(movie_script)
				if (result != 0):
					logger.error("Movie render command failed :: {0}".format(movie_script))
				
				# upload the results ?
				if (len(config.s3_destination) > 0 and running_locally == False):
					upload_path = swap_tokens(tokens, data_row, config.s3_destination)
					upload_path = "{0}/{1}".format(upload_path, movie_name)
					upload_path = upload_path.lower()
					logger.info("Uploading movie to :: {0}".format(upload_path))
					if (not upload_file_to_S3("{0}/{1}".format(local_output, movie_name), upload_path, True)):
						logger.error("Failed to upload movie to :: {0}".format(upload_path))

			# do we make a snapshot?
			# this is only possible if we have a rendered movie
			if (config.create_snapshot):
				logger.info("Creating snapshot")
				snapshot = this_script.render_snapshot()
				snapshot_name = snapshot[0]
				snapshot_script = snapshot[1]
				snapshot_local_path = "{0}/{1}".format(local_output, snapshot_name)
				
				# actually execute the command
				result = os.system(snapshot_script)
				if (result != 0):
					logger.error("Snapshot render command failed :: {0}".format(snapshot_script))
				
				# upload the results ?
				if (len(config.s3_destination) > 0 and running_locally == False):
					upload_path = swap_tokens(tokens, data_row, config.s3_destination)
					upload_path = "{0}/{1}".format(upload_path, snapshot_name)
					upload_path = upload_path.lower()
					logger.info("Uploading snapshot to :: {0}".format(upload_path))
					if (not upload_file_to_S3(snapshot_local_path, upload_path, True)):
						logger.error("Failed to upload snapshot to :: {0}".format(upload_path))
						
			# clean up movies and snapshots?
			if (len(config.s3_destination) > 0 and running_locally == False):
				logger.info("Cleaning up local movie and snapshot files")
				
				for movie in movies:
					movie_name = "{0}/{1}".format(local_output , movie[0])
					# and delete the local if we're uploading
					logger.info("Deleting local movie :: {0}".format(movie_name))
					if (os.path.exists(movie_name)):
						os.remove(movie_name)
					
				if (os.path.exists(snapshot_local_path) and config.create_snapshot):
					logger.info("Deleting local snapshot :: {0}".format(snapshot_local_path))
					os.remove(snapshot_local_path)

		if (config.create_html):
			logger.info("Creating html")
			html_output_name = swap_tokens_html(tokens, data_row, config.html_output_file)
			this_html_template = swap_tokens_html(tokens, data_row, html_template)
			html_local_destination = "{0}/{1}".format(local_output, html_output_name)
			# clean up first to be super sure we don't ever upload the wrong personalised file for someone
			if (os.path.exists(html_local_destination)):
				os.remove(html_local_destination)
			
			# write the transformed template back out
			with open(html_local_destination, "w") as f:
				f.write(this_html_template)

			# upload to s3?
			if (len(config.s3_destination) > 0 and running_locally == False):
				upload_path = swap_tokens_html(tokens, data_row, config.s3_destination)
				upload_path = "{0}/{1}".format(upload_path, html_output_name)
				upload_path = upload_path.lower()
				logger.info("Uploading html to :: {0}".format(upload_path))
				if (not upload_file_to_S3(html_local_destination, upload_path, True)):
					logger.error("Failed to upload html to :: {0}".format(upload_path))

				# delete local copy?
				if (os.path.exists(html_local_destination)):
					os.remove(html_local_destination)

		# iframe template?
		if (config.create_html and len(config.iframe_output_file) > 0):

			logger.info("Creating iframe html")
			iframe_output_name = swap_tokens_html(tokens, data_row, config.iframe_output_file)
			this_iframe_template = swap_tokens_html(tokens, data_row, iframe_template)
			iframe_local_destination = "{0}/{1}".format(local_output, iframe_output_name)
			# clean up first to be super sure we don't ever upload the wrong personalised file for someone
			if (os.path.exists(iframe_local_destination)):
				os.remove(iframe_local_destination)
			
			# write the transformed template back out
			with open(iframe_local_destination, "w") as f:
				f.write(this_iframe_template)

			# upload to s3?
			if (len(config.s3_destination) > 0 and running_locally == False):
				upload_path = swap_tokens_html(tokens, data_row, config.s3_destination)
				upload_path = "{0}/{1}".format(upload_path, iframe_output_name)
				upload_path = upload_path.lower()
				logger.info("Uploading iframe to :: {0}".format(upload_path))
				if (not upload_file_to_S3(iframe_local_destination, upload_path, True)):
					logger.error("Failed to upload iframe to :: {0}".format(upload_path))

				# delete local copy?
				if (os.path.exists(iframe_local_destination)):
					os.remove(iframe_local_destination)
	except Exception as e:
		logger.error(traceback.format_exc())
		#logger.error("Failed to process row :: {}".format(e.stack_trace))
		
if (not running_locally):
	log_file_path = "{0}/{1}".format(config.s3_logs, log_file)
	logger.info("Uploading log to :: {0}".format(log_file_path))
	upload_file_to_S3(log_file, log_file_path)

logger.info("Run completed")

if (running_on_ec2 and config.terminate_on_completion):
	print "terminating instance :: {}".format(instance_id)
	ec2 = boto.ec2.connect_to_region('eu-west-1')
	ec2.terminate_instances(instance_ids=[instance_id])
	print "dying now...."