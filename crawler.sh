#! /bin/bash

URL="https://scholar.google.com/scholar?q=rtxi"

#while $ERROR; do
#	curl -sA "Chrome" -k -L $URL | ./crawler.py
#done

curl -sA "Chrome" -k -L $URL | ./crawler.py
