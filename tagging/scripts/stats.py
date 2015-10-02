"""Print corpus statistics.

Usage:
  stats.py
  stats.py -h | --help

Options:
  -h --help     Show this screen.
"""
from docopt import docopt
from collections import defaultdict
from corpus.ancora import SimpleAncoraCorpusReader


if __name__ == '__main__':
    opts = docopt(__doc__)

    # Load the data
    corpus = SimpleAncoraCorpusReader('ancora/ancora-2.0/')
    sents = corpus.tagged_sents()

    # Compute the statistics

    # Sents
    print('Sents: {}'.format(len(sents)))

    # Words and Tags
    words = []

    # Counted tags
    counted_tags = defaultdict(int)

    # Counted words for each tag
    counted_tag_words = defaultdict(lambda: defaultdict(int))

    for sent in sents:
        for w, t in sent:
            words.append(w)
            counted_tags[t] += 1
            counted_tag_words[t][w] += 1

    word_ocurrences = len(words)
    vocab_w = set(words)

    counted_tags = list(counted_tags.items())
    counted_tags.sort(key=lambda x: x[1], reverse=True)

    # Total num of tags
    total_tags = sum([x[1] for x in counted_tags])

    print('Tokens: {}'.format(word_ocurrences))
    print('Words: {}'.format(len(vocab_w)))
    print('Tags: {}'.format(len(counted_tags)))

    # Most frequent tags
    print("\n10 most frequent tags:\n")
    print("Tag | Freq  |   %   | 5 most frequent words")
    print("-------------------------------------------")
    for i in range(10):
        tag = counted_tags[i][0]
        freq = counted_tags[i][1]
        perc = freq / total_tags * 100
        lw = list(counted_tag_words[tag].items()) # List of words with tag
        lw.sort(key = lambda x: x[1], reverse=True)
        mfw = [x[0] for x in lw[:5]]  # 5 most freq words with tag
        print(tag + "  | {0} | {1:>5.2f} | {2}".format(freq, perc, mfw))
