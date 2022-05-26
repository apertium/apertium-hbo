#!/bin/bash

grep '<v>' ana_unk.txt | sed -E 's/.*\[//g' | sed -E 's/<v>.*/<v>/g' | sed -E 's/.*\+//g' | sort | uniq -c | sort -nr | head