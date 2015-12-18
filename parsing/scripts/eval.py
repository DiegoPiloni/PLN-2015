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

from corpus.ancora_dep import SimpleAncoraDepCorpusReader


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
    files = ["3LB-CAST/*.csv"]
    corpus = SimpleAncoraDepCorpusReader('ancora/ancora-dep-2.0/', files)
    sents = corpus.parsed_sents()

    # Accuracies
    hits, total, acc = 0, 0, 0

    n = len(sents)

    for i, sent in enumerate(sents):
        word_sent, _, pos_sent, gold_dep_sent = zip(*sent)

        word_pos_sent = list(zip(word_sent, pos_sent))

        model_actions_sent = model.actions(word_pos_sent)

        # construct dependency tree from actions
        model_dep_sent = ["0"] * len(word_sent)

        ROOT = ["0", "ROOT"]
        stack = [ROOT]
        buf = [[str(i+1), w] for i, w, in enumerate(word_sent)]

        for action in model_actions_sent:
            if action == "SHIFT":
                top_of_buffer = buf[0]
                buf = buf[1:]
                stack = stack + [top_of_buffer]
            elif action == "REDUCE":
                stack = stack[:-1]
            elif action == "LEFT ARC":
                top_of_buffer = buf[0]
                wi = top_of_buffer[0]
                wj = stack[-1][0]
                model_dep_sent[int(wj)-1] = wi
                stack = stack[:-1]
            elif action == "RIGHT ARC":
                top_of_buffer = buf[0]
                wj = top_of_buffer[0]
                wi = stack[-1][0]
                model_dep_sent[int(wj)-1] = wi
                buf = buf[1:]
                stack = stack + [top_of_buffer]

        assert len(model_dep_sent) == len(gold_dep_sent)

        model_gold_ts = list(zip(model_dep_sent, gold_dep_sent))
        # global score
        hits_sent = [m == g for m, g in model_gold_ts]
        hits += sum(hits_sent)
        total += len(sent)
        acc = float(hits) / total

        progress('{:3.1f}% (Global: {:2.2f}%)'.format(float(i)*100/n, acc*100))

    # Accuracies
    print('\nGlobal Accuracy: {:2.2f}%'.format(acc * 100))
