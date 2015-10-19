from featureforge.vectorizer import Vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from tagging.features import *
from collections import namedtuple, defaultdict


History = namedtuple('History', 'sent prev_tags i')


class MEMM:

    def __init__(self, n, tagged_sents, classifier='logistic_regression'):
        """
        n -- order of the model.
        tagged_sents -- list of sentences, each one being a list of pairs.
        """
        self.n = n
        self.tagged_sents = tagged_sents

        # posible classifiers
        classifiers = {'logistic_regression': LogisticRegression(), \
                       'multinomial_nb': MultinomialNB(), \
                       'linear_svc': LinearSVC()}

        self.vocab = set()
        self.tag_counts = defaultdict(int)
        for tagged_sent in tagged_sents:
            for word, tag in tagged_sent:
                self.vocab.add(word)
                self.tag_counts[tag] += 1

        # Features
        self.features = [word_lower, word_istitle, word_isupper, word_isdigit]
        prev_word = [PrevWord(f) for f in self.features]
        n_prev_tags = [NPrevTags(i) for i in range(1,n)]
        self.features += n_prev_tags + prev_word

        # Pipeline for tag classifier
        self.tag_clf = Pipeline([('vect', Vectorizer(self.features)), \
                                 ('clf', classifiers[classifier]), \
                                ])

        sents_histories = self.sents_histories(tagged_sents)
        sents_tags = self.sents_tags(tagged_sents)

        self.tag_clf = self.tag_clf.fit(sents_histories, sents_tags)

    def sents_histories(self, tagged_sents):
        """
        Iterator over the histories of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        hs = list()
        for tagged_sent in tagged_sents:
            hs += self.sent_histories(tagged_sent)
        return hs

    def sent_histories(self, tagged_sent):
        """
        Iterator over the histories of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        n = self.n
        start = ("<s>",) * (n-1)
        word_sent, tag_sent = zip(*tagged_sent)
        word_sent = list(word_sent)
        tag_sent = start + tag_sent
        hs = list()
        for i in range(len(word_sent)):
            hs.append(History(word_sent, tag_sent[i:i+n-1], i))
        return hs

    def sents_tags(self, tagged_sents):
        """
        Iterator over the tags of a corpus.

        tagged_sents -- the corpus (a list of sentences)
        """
        tags = tuple()
        for tagged_sent in tagged_sents:
            tags += self.sent_tags(tagged_sent)
        return tags

    def sent_tags(self, tagged_sent):
        """
        Iterator over the tags of a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        word_sent, tag_sent = zip(*tagged_sent)
        return tag_sent

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        tagging = list()
        n = self.n
        prev_tags = ("<s>",) * (n-1)
        for i in range(len(sent)):
            hi = History(sent[:i+1], prev_tags, i)
            tag = self.tag_history(hi)
            tagging.append(tag)
            prev_tags = (prev_tags + (tag,))[1:]
        return tagging

    def tag_history(self, h):
        """Tag a history.

        h -- the history.
        """
        predicted_tag = self.tag_clf.predict([h])[0]
        return predicted_tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        unknown = True
        if w in self.vocab:
            unknown = False
        return unknown
