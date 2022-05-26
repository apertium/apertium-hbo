#!/bin/bash

./get_corpus.py

cat ana.txt | sed -e 's/\^//g' -e 's/\//[/g' -e 's/\$/]/g' | apertium -f none -d .. hbo-morph | grep '\*' > ana_unk.txt

cat ana_unk.txt | sed -E -e 's/.*\[//g' -e 's/\]//g' | sed -E 's/\+/\n/g' | sed -E 's/><.*/>/g' | sort | uniq -c | sort -nr | head -n20
