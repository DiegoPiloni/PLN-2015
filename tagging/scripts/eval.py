"""Evaulate a tagger.

Usage:
  eval.py -i <file>
  eval.py -h | --help

Options:
  -i <file>     Tagging model file.
  -h --help     Show this screen.
"""
from docopt import docopt
import pickle
import sys

from corpus.ancora import SimpleAncoraCorpusReader


def progress(msg, width=None):
    """Ouput the progress of something on the same line."""
    if not width:
        width = len(msg)
    print('\b' * width + msg, end='')
    sys.stdout.flush()


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load the model
    filename = opts['-i']
    f = open(filename, 'rb')
    model = pickle.load(f)
    f.close()

    # load the data
    files = '3LB-CAST/.*\.tbf\.xml'
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/', files)
    sents = corpus.tagged_sents()

    # tag
    hits, total = 0, 0
    k_hits, k_total = 0, 0
    u_hits, u_total = 0, 0
    n = len(sents)
    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        # global score
        hits_sent = [m == g for m, g in zip(model_tag_sent, gold_tag_sent)]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total
        progress('{:3.1f}% ({:2.2f}%)'.format(float(i) * 100 / n, acc * 100))

        # known words score
        z = zip(word_sent, model_tag_sent, gold_tag_sent)
        k_sent = [(w, m, g) for w, m, g in z if not model.unknown(w)]
        k_hits_sent = [m == g for w, m, g in k_sent]
        k_hits += sum(k_hits_sent)
        k_total += len(k_sent)

        # unknown words score
        z = zip(word_sent, model_tag_sent, gold_tag_sent)
        u_sent = [(w, m, g) for w, m, g in z if model.unknown(w)]
        u_hits_sent = [m == g for w, m, g in u_sent]
        u_hits += sum(u_hits_sent)
        u_total += len(u_sent)

    acc = float(hits) / total
    k_acc = 0
    u_acc = 0
    if k_total != 0:
        k_acc = float(k_hits) / k_total
    if u_total != 0:
        u_acc = float(u_hits) / u_total

    print('')
    print('Global Accuracy: {:2.2f}%'.format(acc * 100))
    print('Known Words Accuracy: {:2.2f}%'.format(k_acc * 100))
    print('Unknown Words Accuracy: {:2.2f}%'.format(u_acc * 100))
