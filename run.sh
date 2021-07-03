#!/bin/bash
/home/eleonorvinicius/Projects/imdbsurfer/./imdbsurfer.sh > /home/eleonorvinicius/Projects/imdbsurfer/imdbsurfer.log 2>&1 &
tail -f /home/eleonorvinicius/Projects/imdbsurfer/imdbsurfer.log
