# apertium-hbo Evaluation Scripts

The scripts are for evaluating the current state of the analyzer.
They rely on comparison to the [Biblia Hebraica Stuttgartensia Amstelodamensis](https://etcbc.github.io/bhsa/) via [text-fabric](https://annotation.github.io/text-fabric/tf/index.html) library.

To get the corpus data for the first time, run

```python
from tf.app import use                    # import the library
A = use('etcbc/bhsa')                     # open or download the data
A.extract({'GenesisBook': ('genesis',)})  # extract just Genesis
```

The scripts currently operate on only Genesis. This can be changed by editing `get_corpus.py`.

Once you have the data, running `make` will produce several text files, including

* `ana.txt` - the BHSA in Apertium format, one token per line
* `ana_morph.txt` - `ana.txt` with the current analyzer output
* `coverage.txt` - the most frequent unknown words and naïve coverage
* `precision.txt` - the precision, recall, and F1 scores
