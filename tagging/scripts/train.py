"""Train a sequence tagger.

Usage:
  train.py [-m <model>] [-n <n>] [-c <classifier>] -o <file>
  train.py -h | --help

Options:
  -m <model>        Model to use [default: base]:
                        base: Baseline
                        mlhmm: Max. Likelihood Hidden Markov Model
                        memm: Max. Entropy Markov Model
  -n <n>            n-gram for mlhmm/memm.
  -c <classifier> Classifier to use for memm [default: logistic_regression]
                        lr: Max ent. classifier (Logistic Regression)
                        mnb: Multinomial Naive Bayes
                        lsvc: Linear Support Vector Classification
  -o <file>         Output model file.
  -h --help         Show this screen.
"""
from docopt import docopt
import pickle
import sys
from corpus.ancora import SimpleAncoraCorpusReader
from tagging.baseline import BaselineTagger
from tagging.hmm import MLHMM
from tagging.memm import MEMM


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the data
    files = 'CESS-CAST-(A|AA|P)/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = corpus.tagged_sents()

    sents = [s for s in sents if s != []]

    # train the model
    if opts['-m'] == 'base':
        model = BaselineTagger(sents)
    elif opts['-m'] == "memm":
        n = int(opts['-n'])
        clf = "lr"
        if opts['-c']:
            clf = opts['-c']
        model = MEMM(n, sents, clf)
    elif opts['-m'] == "mlhmm":
        n = int(opts['-n'])
        model = MLHMM(n, sents)
    else:
        sys.exit("ERROR: Unknown model")

    # save it
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
