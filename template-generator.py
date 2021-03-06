#!/usr/bin/python

# requires 
# urllib3, python-pip
# pip install boto BeautifulSoup

import sys
import os

from FFMPEG import DrawText
from FFMPEG import FFMPEG
from FFMPEG import Encoder

font = "%_CWD_%/materials/roboto_ttf/Roboto-Black.ttf"
movie = FFMPEG("JG 008 Animatic with TEXTLESS.mp4", "%_FundraiserGuid_%")
movie.input_flags = "-strict -2"
movie.snapshot_timestamp = "00:00:03.123"
movie.snapshot_name = "%_FundraiserGuid_%.png"

webm = Encoder("webm", "-c:v libvpx -quality good -cpu-used 2 -qmin 10 -qmax 42 -crf 18 -b:v 1M -c:a libvorbis -threads 4")
mp4 = Encoder("mp4", "-profile:v main -level 3.1 -c:v libx264 -preset slow -crf 22")
movie.output_encoders.append(webm)
movie.output_encoders.append(mp4)

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
