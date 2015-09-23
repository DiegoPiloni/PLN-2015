"""
Train an n-gram model.

Usage:
  train.py -n <n> [-m <model>] -o <file> [-g <file>]
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <model>    Model to use [default: ngram]:
                  ngram: Unsmoothed n-grams.
                  addone: N-grams with add-one smoothing.
                  interpolated: N-grams with linear interpolation smoothing.
                  backoff: N-grams with discounting (Back-off) smoothing.
  -o <file>     Output model file.
  -g <file>     Output generator file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import gutenberg, PlaintextCorpusReader
from languagemodeling.ngram import NGram, AddOneNGram, InterpolatedNGram, BackOffNGram, NGramGenerator


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = gutenberg.sents(gutenberg.fileids().remove("austen-persuasion.txt"))
    # sents = gutenberg.sents("austen-emma.txt")
    # sents = sents[:int(90*len(sents)/100)]

    # train the model
    n = int(opts['-n'])
    m = (opts['-m']).lower()

    if m == "addone":
        model = AddOneNGram(n, sents)
    elif m == "interpolated":
        model = InterpolatedNGram(n, sents)
    elif m == "backoff":
        model = BackOffNGram(n, sents)
    else:
        model = NGram(n, sents)

    # save the model
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()

    # train generator (optional)
    if opts['-g']:
        generator = NGramGenerator(model)

        # save generator
        filename = opts['-g']
        f = open(filename, 'wb')
        pickle.dump(generator, f)
        f.close()
