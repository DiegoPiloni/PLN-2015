"""Train a parser.

Usage:
  train.py [-c <classifier>] -o <file>
  train.py -h | --help

Options:
  -c <classifier>  Classifier to use [default: svm]
                        lr: Max ent. classifier (Logistic Regression)
                        svm: Linear Support Vector Classification
  -o <file>   Output model file.
  -h --help   Show this screen.
"""

from docopt import docopt
import sys
import pickle

from corpus.ancora_dep import SimpleAncoraDepCorpusReader

from parsing.tb_dependency_parser import TBDependencyParser

classifiers = ["svm", "lr"]

if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading corpus...')
    files = ["CESS-CAST-A/*.csv", "CESS-CAST-AA/*.csv", "CESS-CAST-P/*.csv"]

    corpus = SimpleAncoraDepCorpusReader('ancora/ancora-dep-2.0/', files)

    parsed_sents = corpus.parsed_sents()

    print('Training model...')
    if opts['-c'] is not None:
        if opts['-c'] in classifiers:
            clf = opts['-c']
        else:
            sys.exit("ERROR: Unknown classifier")
    else:
        clf = "svm"

    model = TBDependencyParser(parsed_sents, clf)

    print('Saving...')
    filename = opts['-o']
    f = open(filename, 'wb')
    pickle.dump(model, f)
    f.close()
