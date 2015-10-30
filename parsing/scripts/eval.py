"""Evaulate a parser.

Usage:
  eval.py -i <file> [-m <m>] [-n <n>]
  eval.py -h | --help

Options:
  -i <file>     Parsing model file.
  -m <m>        Only evaluate sents with length <= m
  -n <n>        Only evaluate the first n sents.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader

from parsing.util import spans


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    print('Loading model...')
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    print('Loading corpus...')
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    parsed_sents = list(corpus.parsed_sents())

    # check -n option
    if opts['-n'] is not None:
        n = int(opts['-n'])
        parsed_sents = parsed_sents[:n]

    # check -m option
    if opts['-m'] is not None:
        m = int(opts['-m'])
        parsed_sents = [ps for ps in parsed_sents if len(ps.leaves()) <= m]

    n = len(parsed_sents)

    print('Parsing...')
    lab_hits, unlab_hits, total_gold, total_model = 0, 0, 0, 0
    format_str = '{:3.1f}% ({}/{}) (LP={:2.2f}%, LR={:2.2f}%, LF1={:2.2f}%) (ULP={:2.2f}%, ULR={:2.2f}%, ULF1={:2.2f}%)'
    progress(format_str.format(0.0, 0, n, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0))
    for i, gold_parsed_sent in enumerate(parsed_sents):
        tagged_sent = gold_parsed_sent.pos()

        # parse
        model_parsed_sent = model.parse(tagged_sent)

        # compute labeled scores
        lab_gold_spans = spans(gold_parsed_sent, unary=False)
        lab_model_spans = spans(model_parsed_sent, unary=False)
        lab_hits += len(lab_gold_spans & lab_model_spans)

        # compute unlabeled scores
        unlab_gold_spans = set([s[1:] for s in lab_gold_spans])
        unlab_model_spans = set([s[1:] for s in lab_model_spans])
        unlab_hits += len(unlab_gold_spans & unlab_model_spans)

        # total spans
        total_gold += len(lab_gold_spans)
        total_model += len(lab_model_spans)

        # compute labeled partial results
        lab_prec = float(lab_hits) / total_model * 100
        lab_rec = float(lab_hits) / total_gold * 100
        lab_f1 = 2 * lab_prec * lab_rec / (lab_prec + lab_rec)

        # compute unlabeled partial results
        unlab_prec = float(unlab_hits) / total_model * 100
        unlab_rec = float(unlab_hits) / total_gold * 100
        unlab_f1 = 2 * unlab_prec * unlab_rec / (unlab_prec + unlab_rec)

        progress(format_str.format(float(i+1) * 100 / n, i+1, n, lab_prec, lab_rec, lab_f1, unlab_prec, unlab_rec, unlab_f1))

    print('')
    print('Parsed {} sentences'.format(n))
    print('Labeled')
    print('  Precision: {:2.2f}% '.format(lab_prec))
    print('  Recall: {:2.2f}% '.format(lab_rec))
    print('  F1: {:2.2f}% '.format(lab_f1))
    print('Unlabeled')
    print('  Precision: {:2.2f}% '.format(unlab_prec))
    print('  Recall: {:2.2f}% '.format(unlab_rec))
    print('  F1: {:2.2f}% '.format(unlab_f1))
