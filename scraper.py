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
url = "https://scholar.google.com/scholar?q=rtxi"
terms = [ 'rtxi', 'RTXI', 'real-time experiment interface']

################################################################################
# Initialize buffers and download initial page
################################################################################
buffer = BytesIO()
curl = pycurl.Curl()
curl.setopt(pycurl.URL, url)
curl.setopt(pycurl.SSL_VERIFYPEER, 1)
curl.setopt(pycurl.SSL_VERIFYHOST, 2)
curl.setopt(curl.WRITEDATA, buffer)

# download the page and write bytecode to buffer
curl.perform()
curl.close()
html = buffer.getvalue().decode('iso-8859-1')

################################################################################
# Set up parser and find links
################################################################################
soup = BeautifulSoup(html, 'html.parser')
anchor_tags = soup.find_all("a")

anchor_text = [ a.getText() for a in anchor_tags ]
