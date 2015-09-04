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
  -o <file>     Output model file.
  -g <file>     Output generator file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import gutenberg, PlaintextCorpusReader
from languagemodeling.ngram import NGram, AddOneNGram, NGramGenerator


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    my_corpus = PlaintextCorpusReader('../corpus/', '.*\.txt')
    sents = my_corpus.sents()

    # train the model
    n = int(opts['-n'])
    m = (opts['-m'])

    if m != "addone":
        model = NGram(n, sents)
    else:
        model = AddOneNGram(n, sents)

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
