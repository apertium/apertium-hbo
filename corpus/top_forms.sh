#!/bin/bash

grep "$1<v>" ana_unk.txt | sed -E 's/.*\[//g' | sort | uniq -c | sort -nr
