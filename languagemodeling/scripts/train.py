"""Train an n-gram model.

Usage:
  train.py -n <n> -m <file> [-g <file>]
  train.py -h | --help

Options:
  -n <n>        Order of the model.
  -m <file>     Output model file.
  -g <file>     (Optional) Output generator file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle

from nltk.corpus import gutenberg

from languagemodeling.ngram import NGram, NGramGenerator


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    sents = gutenberg.sents('austen-emma.txt')

    # train the model
    n = int(opts['-n'])
    model = NGram(n, sents)

    # save the model
    filename = opts['-m']
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
