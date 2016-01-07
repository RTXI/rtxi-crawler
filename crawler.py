#! /bin/env python

from bs4 import BeautifulSoup
from io import BytesIO
import pycurl
import sqlite3 as sql
import sys
import re

################################################################################
# Global variables
################################################################################
url_queue = ["https://scholar.google.com/scholar?q=rtxi"]
terms = ['rtxi', 'RTXI', '(R|r)eal( |-)time (e|E)(X|x)periment (I|i)nterface']

################################################################################
# Functions
################################################################################
def parse_html(html):
    soup = BeautifulSoup(html, "html.parser")
    anchor_tags = soup.find_all("a")
    anchor_links = []
    anchor_text = []
    for a in anchor_tags:
        try: 
            anchor_links.append(a['href'])
            anchor_text.append(a.getText())
        except KeyError:
            print(a)
    return (anchor_text, anchor_links)

def filter_links(text, links, terms):
    findings = [ (text[i], links[i]) for i in range(len(text)) 
                 for term in terms if re.search(term, text[i]) ]
    return findings

################################################################################
# Initialize buffers and download initial page
################################################################################
buffer = BytesIO()
curl = pycurl.Curl()
curl.setopt(pycurl.URL, url_queue[0])
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(curl.WRITEDATA, buffer)

# download the page and write bytecode to buffer
curl.perform()
curl.close()
html = buffer.getvalue().decode('iso-8859-1')

################################################################################
# Parse HTML and get new links
################################################################################
text, links = parse_html(html)
tuples = filter_links(text, links, terms)

for thing in tuples:
    print(thing)


################################################################################
# Unused code
################################################################################
#[ item for item in text for term in terms if re.search(term, item) ]
