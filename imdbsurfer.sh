#!/bin/bash
date
cd /home/eleonorvinicius/Projects/imdbsurfer
source bin/activate
scrapy crawl movies > movies.log 2>&1
python3 Main.py
date