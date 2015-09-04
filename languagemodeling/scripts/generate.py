"""Generate sentences from an n-gram model.

Usage:
  generate.py -s <n> -i <file>
  generate.py -h | --help

Options:
  -s <n>        Amount of sentences.
  -i <file>     Input generator trained file.
  -h --help     Show this screen.
"""
from docopt import docopt
from languagemodeling.ngram import NGramGenerator
import pickle


if __name__ == '__main__':
    opts = docopt(__doc__)

    # load generator from input
    input_filename = opts['-i']
    input_file = open(input_filename, 'rb')
    ngramGen = pickle.load(input_file)
    input_file.close()

    a_s = int(opts['-s'])
    gen_sents = ""
    for i in range(a_s):
        gen_sent = ngramGen.generate_sent()
        gen_sents += (" ".join(gen_sent))
        if i != a_s - 1:
            gen_sents += '\n'

    print(gen_sents)
