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

from FFMPEG import DrawText


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

def HTMLEntitiesToUnicode(text):
    """Converts HTML entities to unicode.  For example '&amp;' becomes '&'."""
    text = unicode(BeautifulStoneSoup(text, convertEntities=BeautifulStoneSoup.HTML_ENTITIES))
    return text.encode("utf-8")

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


tokenlist_file = 'data.definition'
logger.info("Loading token list from {0}".format(tokenlist_file))
tokens = LoadTokenList(tokenlist_file)
logger.info("Loaded {0} tokens".format( len( tokens ) ) )


text_object = DrawText("demo text", 500, 1500)
print text_object


#data_file = 'PageReportV2.csv'
#for row in CsvDataIterator(data_file):
#    row[4] = HTMLEntitiesToUnicode(BeautifulSoup(row[4]).getText())
    #logger.debug(row)

