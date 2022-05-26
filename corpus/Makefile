all: coverage.txt precision.txt verb_unk.txt noun_unk.txt

ana.txt: get_corpus.py
	./get_corpus.py

ana_morph.txt: ana.txt ../hbo.automorf.hfst
	cat $< | sed -E -e 's/\^//g' -e 's/\//\[/g' -e 's/\$$/]/g' | apertium -f none -d .. hbo-morph > $@

ana_unk.txt: ana_morph.txt
	cat $^ | grep '\*' > $@

verb_unk.txt: ana_unk.txt
	grep '<v>' ana_unk.txt | sed -E 's/.*\[//g' | sed -E 's/<v>.*/<v>/g' | sed -E 's/.*\+//g' | sort | uniq -c | sort -nr > $@

noun_unk.txt: ana_unk.txt
	grep '<n>' ana_unk.txt | sed -E 's/.*\[//g' | sed -E 's/<n>.*/<n>/g' | sed -E 's/.*\+//g' | sort | uniq -c | sort -nr > $@

coverage.txt: ana.txt ../hbo.automorf.hfst
	./coverage.sh > $@

precision.txt: ana_morph.txt precision.py
	./precision.py > $@

SHELL=/bin/bash
