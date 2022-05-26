#!/bin/bash

TMPCORPUS=raw.txt
TMPPARADE=parade.txt

#cat $TMPCORPUS | lt-proc ../hbo.automorf.bin > $TMPPARADE
cat $TMPCORPUS | apertium -f none -d .. hbo-morph > $TMPPARADE

cat $TMPPARADE | grep '\*' | sort | uniq -c | sort -rn | head -n30

TOTAL=`grep -v '^$' $TMPPARADE | wc -l`
KNOWN=`grep -v '^$' $TMPPARADE | grep -v '\*' | wc -l`
UNKNOWN=`grep -v '^$' $TMPPARADE | grep '\*' | wc -l`

PERCENTAGE=`echo $KNOWN/$TOTAL | calc -p | sed 's/[\s\t]//g'`

echo "coverage: $KNOWN / $TOTAL ($PERCENTAGE)"
echo "remaining unknown forms: $UNKNOWN"
