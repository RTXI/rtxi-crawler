#! /bin/env python

from bs4 import BeautifulSoup
from io import BytesIO
import pycurl
import re
import time
import random
#import sqlite3 as sql

################################################################################
# Global variables
################################################################################
url_queue = ["https://scholar.google.com/scholar?q=rtxi", 
             "http://link.springer.com/search?query=rtxi" ]
all_results = []
terms = [ 'rtxi', 'real( |-)time experiment interface']

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
   findings = [ [text[i], links[i]] for i in range(len(text)) 
                for term in terms if re.search(term, text[i], re.IGNORECASE) 
                if '.pdf' not in links[i] ]
   for idx in range(len(findings)):
      if findings[idx][1][0:4] != 'http':
         findings[idx][1] = 'http:/' + findings[idx][1]
   return findings

def download_page(url):
   buffer = BytesIO()
   curl = pycurl.Curl()
   curl.setopt(pycurl.URL, url)
   curl.setopt(pycurl.SSL_VERIFYPEER, 1)
   curl.setopt(pycurl.SSL_VERIFYHOST, 2)
   curl.setopt(curl.WRITEDATA, buffer)
   curl.setopt(curl.FOLLOWLOCATION, True)
   curl.perform()
   print(curl.getinfo(pycurl.HTTP_CODE), curl.getinfo(pycurl.EFFECTIVE_URL))
   curl.close()
   html = buffer.getvalue().decode('iso-8859-1')
   time.sleep(5+random.randrange(0,10)) # good manners
   return html

################################################################################
# Main body
################################################################################

idx = 0
while url_queue and idx < 10:
   url = url_queue.pop(0)
   print("Downloading ", url)
   html = download_page(url)
   text, links = parse_html(html)
   results = filter_links(text, links, terms)
   print("Found links: ", [ result[1] for result in results ])
   url_queue = url_queue + [ result[1] for result in results ]
   all_results = all_results + results
   idx += 1

print("steps: ", idx)
print("found: ", results)

################################################################################
# Unused code
################################################################################

