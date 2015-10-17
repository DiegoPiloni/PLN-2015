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

from collections import defaultdict
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
    sents = list(corpus.tagged_sents())

    # Accuracies and Confusion "Matrix"
    hits, total = 0, 0
    k_hits, k_total = 0, 0
    u_hits, u_total = 0, 0
    acc, k_acc, u_acc = 0, 0, 0
    c_tags = list(model.tag_counts.items())  # counted tags
    confusion = defaultdict(lambda: defaultdict(int))  # confusion "matrix"
    n = len(sents)

    for i, sent in enumerate(sents):
        word_sent, gold_tag_sent = zip(*sent)

        model_tag_sent = model.tag(word_sent)
        assert len(model_tag_sent) == len(gold_tag_sent), i

        model_gold_ts = list(zip(model_tag_sent, gold_tag_sent))
        # global score
        hits_sent = [m == g for m, g in model_gold_ts]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        # known words score
        z = list(zip(word_sent, model_tag_sent, gold_tag_sent))
        k_sent = [(w, m, g) for w, m, g in z if not model.unknown(w)]
        k_hits_sent = [m == g for w, m, g in k_sent]
        k_hits += sum(k_hits_sent)
        k_total += len(k_sent)
        if k_total != 0:
            k_acc = float(k_hits) / k_total

        # unknown words score
        u_sent = [(w, m, g) for w, m, g in z if model.unknown(w)]
        u_hits_sent = [m == g for w, m, g in u_sent]
        u_hits += sum(u_hits_sent)
        u_total += len(u_sent)
        if u_total != 0:
            u_acc = float(u_hits) / u_total

        progress('{:3.1f}% (G: {:2.2f}%) (K: {:2.2f}%) (U: {:2.2f}%)'.format(
            float(i) * 100 / n, acc * 100, k_acc * 100, u_acc * 100))

        # confusion "matrix"
        unhits_sent = [(m, g) for m, g in model_gold_ts if m != g]
        for m, g in unhits_sent:
            confusion[g][m] += 1

    # Accuracies
    print('\nGlobal Accuracy: {:2.2f}%'.format(acc * 100))
    print('Known Words Accuracy: {:2.2f}%'.format(k_acc * 100))
    print('Unknown Words Accuracy: {:2.2f}%'.format(u_acc * 100))

    # Confusion matrix (Could be improved)
    c_tags.sort(key=lambda x: x[1], reverse=True)
    mft = c_tags[:10]  # 10 most frequent tags
    conf_matrix = []
    for i, (tagi, _) in enumerate(mft):
        conf_matrix.append([])
        for j, (tagj, _) in enumerate(mft):
            conf_matrix[i].append(confusion[tagj][tagi])

    print("\nConfusion Matrix")
    for tag, _ in mft:
        print("{0:>8}".format(tag), end="")
    print("")
    for i, (tag, _) in enumerate(mft):
        print(tag + " | ", end=" ")
        for j in range(10):
            print("{0:<5} | ".format(conf_matrix[i][j]), end="")
        print("")
