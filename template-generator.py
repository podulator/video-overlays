#!/usr/bin/python

# requires 
# urllib3, python-pip
# pip install boto BeautifulSoup

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

font = "{0}/roboto_ttf/Roboto-Black.ttf".format(os.getcwd())
movie = FFMPEG("JG 008 Animatic with TEXTLESS.mp4", "outmovie.webm")
movie.snapshot_timestamp = "00:00:03.123"
movie.snapshot_name = "snapshot.png"

first_name_object = DrawText("%FIRST_NAME%", 0, 97)
first_name_object.line_max_length = 50
first_name_object.x = 600
first_name_object.y = 169.99
first_name_object.fix_bounds = True
first_name_object.font.file = font
first_name_object.font.size = 80
first_name_object.box.enabled = False
first_name_object.box.colour = "0000AA99"
first_name_object.box.border_width = 3
first_name_object.clean_content = True

charity_name_object = DrawText('%CHARITY_NAME%', 265, 348)
charity_name_object.line_max_length = 50
charity_name_object.x = 623
charity_name_object.y = 183
charity_name_object.fix_bounds = True
charity_name_object.font.file = font
charity_name_object.font.size = 80
charity_name_object.box.enabled = False
charity_name_object.box.colour = "FF00AA00"
charity_name_object.box.border_width = 3
charity_name_object.clean_content = True

donor_message_1_object = DrawText('%DONOR_MESSAGE_1%', 453, 685)
donor_message_1_object.line_max_length = 30
donor_message_1_object.x = 0
donor_message_1_object.y = 0
donor_message_1_object.fix_bounds = True
donor_message_1_object.font.file = font
donor_message_1_object.font.size = 80
donor_message_1_object.box.enabled = False
donor_message_1_object.box.colour = "FF00AA00"
donor_message_1_object.box.border_width = 3
donor_message_1_object.clean_content = True

donor_message_2_object = DrawText('%DONOR_MESSAGE_2%', 453, 685)
donor_message_2_object.line_max_length = 30
donor_message_2_object.x = 948
donor_message_2_object.y = 557
donor_message_2_object.fix_bounds = True
donor_message_2_object.font.file = font
donor_message_2_object.font.size = 80
donor_message_2_object.box.enabled = False
donor_message_2_object.box.colour = "FF00AA00"
donor_message_2_object.box.border_width = 3
donor_message_2_object.clean_content = True

donor_message_3_object = DrawText('%DONOR_MESSAGE_3%', 819, 1052)
donor_message_3_object.line_max_length = 30
donor_message_3_object.x = 0
donor_message_3_object.y = 0
donor_message_3_object.fix_bounds = True
donor_message_3_object.font.file = font
donor_message_3_object.font.size = 80
donor_message_3_object.box.enabled = False
donor_message_3_object.box.colour = "FF00AA00"
donor_message_3_object.box.border_width = 3
donor_message_3_object.clean_content = True

donor_message_4_object = DrawText('%DONOR_MESSAGE_4%', 819, 1052)
donor_message_4_object.line_max_length = 30
donor_message_4_object.x = 948
donor_message_4_object.y = 557
donor_message_4_object.fix_bounds = True
donor_message_4_object.font.file = font
donor_message_4_object.font.size = 80
donor_message_4_object.box.enabled = False
donor_message_4_object.box.colour = "FF00AA00"
donor_message_4_object.box.border_width = 3
donor_message_4_object.clean_content = True

movie.text_objects.append(first_name_object)
movie.text_objects.append(charity_name_object)
movie.text_objects.append(donor_message_1_object)
movie.text_objects.append(donor_message_2_object)
movie.text_objects.append(donor_message_3_object)
movie.text_objects.append(donor_message_4_object)

template = movie.to_JSON()
print (template)
