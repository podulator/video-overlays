#!/usr/bin/python

# requires
# urllib3, python-pip
# pip install boto BeautifulSoup

import csv
from boto.s3.connection import S3Connection
from BeautifulSoup import BeautifulSoup
from BeautifulSoup import BeautifulStoneSoup
import logging
import sys
import HTMLParser
import re

# logging setup

debugLevel = logging.DEBUG#INFO
logger = logging.getLogger('Video Processor')
logger.setLevel(debugLevel)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
ch = logging.StreamHandler(sys.stdout)
ch.setFormatter(formatter)
ch.setLevel(debugLevel)
logger.addHandler(ch)

def setDebugLevel(val):
    logger.setLevel(val)
    ch.setLevel(val)

# end logging setup


html_parser = HTMLParser.HTMLParser()
cleaner = re.compile("&rsquo;")

def HTMLEntitiesToUnicode(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
    return text.encode("utf-8")

with open('PageReportV2.csv', 'rb') as f:
    reader = csv.reader(f, quotechar='"', delimiter=',', quoting=csv.QUOTE_ALL, skipinitialspace=True)
    for row in reader:
        row[4] = HTMLEntitiesToUnicode(BeautifulSoup(row[4]).getText())
        logger.debug("csv parser :: {0}".format(row[4]))
