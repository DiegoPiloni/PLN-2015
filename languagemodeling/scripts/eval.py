"""
Evaulate a language model using the test set.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Language model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
from nltk.corpus import gutenberg, PlaintextCorpusReader
from languagemodeling.ngram import NGram, AddOneNGram


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load generator from input
    input_filename = opts['-i']
    input_file = open(input_filename, 'rb')
    model = pickle.load(input_file)
    input_file.close()

    # load the data
    # test_data = PlaintextCorpusReader('../corpus/', ['test.txt'])
    # sents = test_data.sents()
    sents = gutenberg.sents('austen-emma.txt')
    sents = sents[int(90*len(sents)/ 100):]
    sents = [s for s in sents if len(s) <= 30] # very long sentences give -inf prob.
    num_words = 0
    for sent in sents:
        num_words += len(sent)

    perplexity = model.perplexity(sents, num_words)
    print(perplexity)