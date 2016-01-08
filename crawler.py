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
parsed_pages = []
unparsed_pages = []
terms = [ 'rtxi', 'real( |-)time experiment interface']


################################################################################
# Define module class
################################################################################

class Paper:
   def __init__(self, link, parent_link=""):
      self.link = self.link
      self.parent_link = parent_link
      self.check_link()

      self.title = ""
      self.authors = []
      self.reference = ""
      self.date = ""
      self.abstract = ""

   def check_link():
      if self.link[0:4] != 'http' and self.link[0] == '/' and parent_link
         blubs = self.parent_link.split("//")
         blubs = [ blub for blub in blubs if blub ]
         blubs = blubs.split("/")
         blubs = [ blub for blub in blubs if blub ]
         tld = blubs[0]
         self.link = tld + self.link
                  
   def print_html():
      slug = slugify(self.title) + ".html"
      f = open(slug, "w")
      f.write("---")
      f.write("title: ", self.title)
      f.write("category: papers")
      f.write("layout: paper")
      f.write("reference: ", self.reference)
      f.write("authors:")
      for author in self.authors:
         f.write(" - ", author)
      f.write("link: ", self.link)
      f.write("---")
      f.write("")
      f.write(self.abstract)
      f.close()
      

################################################################################
# Define global helper functions
################################################################################

def slugify(s):
   s = s.lower()
   for c in [' ', '-', '.', '/']:
       s = s.replace(c, '_')
   s = re.sub('\W', '', s)
   s = s.replace('_', ' ')
   s = re.sub('\s+', ' ', s)
   s = s.strip()
   s = s.replace(' ', '-')
   return s

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
   try:
      curl.perform()
   except:
      print("Download ERROR: ", url)
   curl.close()
   html = buffer.getvalue().decode('iso-8859-1')
   time.sleep(5+random.randrange(0,10)) # good manners
   return html

def is_duplicate(url, all_urls):
   if url in all_urls:
      return true
   else
      return false


################################################################################
# Main body
################################################################################

idx = 0
while url_queue and idx < 10:
   url = url_queue.pop(0)
   #print("Downloading ", url)
   html = download_page(url)
   text, links = parse_html(html)
   results = filter_links(text, links, terms)
   #print("Found links: ", [ result[1] for result in results ])
   url_queue = url_queue + [ result[1] for result in results ]
   all_results = all_results + results
   idx += 1

print("steps: ", idx)
print("found: ", results)


################################################################################
# Unused code
################################################################################


