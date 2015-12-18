import csv
import glob
import os


class SimpleAncoraDepCorpusReader():
    """Ancora dependency corpus with simplified POS tagset."""
    # FIX: NOT LAZY #

    def __init__(self, path, files=None):
        if files is None:
            files = ["*.csv"]
        self.csvreaders = []
        for fs in files:
            for f in glob.glob(os.path.join(path, fs)):
                with open(f, newline='') as csvfile:
                    self.csvreaders.append(list(csv.reader(csvfile,
                                           delimiter=' ', quotechar='|')))

    def parsed_sents(self):
        """Return simplified parsed sents of the corpus"""
        parsed_sents = list()
        for reader in self.csvreaders:
            new_sent = list()
            for sent in reader:
                if sent == []:
                    if new_sent:
                        parsed_sents.append(new_sent)
                        new_sent = []
                else:
                    if sent[0] != '#':
                        if '\t' not in sent:
                            sent = ['\t'.join(sent)]
                        sent = sent[0].split('\t')[1:5]
                        sent[2] = sent[2][:2]
                        new_sent.append(sent)
        return parsed_sents
