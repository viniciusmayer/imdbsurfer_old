#!/bin/bash
echo "ScrapyCrawl begin"
date
inicio=$(date +"%s")
docker start postgres
cd /home/eleonorvinicius/Projects/imdbsurfer
source bin/activate
scrapy crawl movies
python3 Main.py
fim=$(date +"%s")
dif=$(($fim-$inicio))
horas=$(($dif/3600))
minutos=$((($dif%3600)/60))
segundos=$(($dif%60))
echo "ScrapyCrawl end: ${horas}h:${minutos}m:${segundos}s"
date
