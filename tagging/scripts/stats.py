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

    print("\nCorpus Statistics")
    print("-----------------\n")

    # Sents
    print('Sents: {}'.format(len(sents)))

    # Words
    word_ocurrences = 0

    # Counted tags
    counted_tags = defaultdict(int)

    # Counted words for each tag
    counted_tag_words = defaultdict(lambda: defaultdict(int))

    # Tags for each word and counts of each word
    word_tags = defaultdict(lambda: [0, set()])

    for sent in sents:
        for w, t in sent:
            word_ocurrences += 1
            counted_tags[t] += 1
            counted_tag_words[t][w] += 1
            word_tags[w][0] += 1
            word_tags[w][1].add(t)

    vocab_w = len(word_tags)

    counted_tags = list(counted_tags.items())
    counted_tags.sort(key=lambda x: x[1], reverse=True)

    # Total num of tags
    total_tags = sum([x[1] for x in counted_tags])

    print('Tokens: {}'.format(word_ocurrences))
    print('Words: {}'.format(vocab_w))  # set(words) = word vocabulary
    print('Tags: {}'.format(len(counted_tags)))

    # Most frequent tags
    print("\n10 most frequent tags:")
    print("Tag | Freq  |   %   | 5 most frequent words")
    print("-------------------------------------------")
    for i in range(10):
        tag = counted_tags[i][0]
        freq = counted_tags[i][1]
        perc = freq / total_tags * 100
        lw = list(counted_tag_words[tag].items())  # List of words with tag
        lw.sort(key=lambda x: x[1], reverse=True)
        mfw = [x[0] for x in lw[:5]]  # 5 most freq words with tag
        print(tag + "  | {0} | {1:>5.2f} | {2}".format(freq, perc, mfw))

    # Word-types ambiguety
    levels_of_ambiguety = [0] * 9
    for w in word_tags:
        levels_of_ambiguety[len(word_tags[w][1]) - 1] += 1

    print("\nAmbiguety")
    print("Level | Words  | Percentage | 5 Most frequent words")
    print("---------------------------------------------------")
    for i in range(9):  # 9 levels of ambiguety
        words = levels_of_ambiguety[i]
        perc = words / vocab_w * 100
        lwi = [w for w in list(word_tags.items()) if len(w[1][1]) == i+1]
        lwi.sort(key=lambda w: w[1][0], reverse=True)
        lwi = list(map(lambda x: x[0], lwi))
        mfwi = lwi[:5]
        print("{0:<6}| {1:<7}| {2:<11.2f}| {3}".format(i+1, words, perc, mfwi))
