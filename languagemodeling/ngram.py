# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
import random


class NGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)

        for sent in sents:
            sent = ['<s>']*(n-1) + sent + ['</s>']
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                counts[ngram] += 1
                counts[ngram[:-1]] += 1

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        n = self.n
        l_t = len(tokens)
        assert l_t == n or l_t == (n-1)
        return self.counts[tuple(tokens)]

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1
        tokens = prev_tokens + [token]
        return float(self.counts[tuple(tokens)]) / self.counts[tuple(prev_tokens)]

    def sent_prob(self, sent):
        """Probability of a sentence. Warning: subject to underflow problems.
        sent -- the sentence as a list of tokens.
        """
        n = self.n
        new_sent = ['<s>']*(n-1) + sent + ['</s>']
        p = 1
        for i in range(n-1, len(new_sent)):
            cond_p = self.cond_prob(new_sent[i], new_sent[i-n+1:i])
            p *= cond_p
            if p == 0:
                break
        return p

    def sent_log_prob(self, sent):
        """Log-probability of a sentence.
        sent -- the sentence as a list of tokens.
        """
        p = self.sent_prob(sent)
        if p == 0:
            log_p = float('-inf')
        else:
            log_p = log(p, 2)
        return log_p


class AddOneNGram(object):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        assert n > 0
        self.n = n
        self.counts = counts = defaultdict(int)
        self.vocab = []
        self.len_vocab = 0

        for sent in sents:
            sent = ['<s>']*(n-1) + sent + ['</s>']
            for i in range(len(sent) - n + 1):
                ngram = tuple(sent[i: i + n])
                self.vocab += [w for w in ngram if w != '<s>']
                counts[ngram] += 1
                counts[ngram[:-1]] += 1
        self.vocab = list(set(self.vocab))
        self.len_vocab = len(self.vocab)

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        n = self.n
        l_t = len(tokens)
        assert l_t == n or l_t == (n-1)
        return self.counts[tuple(tokens)]

    def cond_prob(self, token, prev_tokens=None):
        """Conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n - 1
        tokens = prev_tokens + [token]
        count_ngram = float(self.counts[tuple(tokens)])
        count_n_1gram = self.counts[tuple(prev_tokens)]
        return (count_ngram + 1) / (count_n_1gram + self.V())

    def V(self):
        """Size of the vocabulary.
        """
        return self.len_vocab


class NGramGenerator(object):

    def __init__(self, model):
        """
        model -- n-gram model.
        """
        self.n = model.n
        self.probs = defaultdict(dict)
        self.sorted_probs = {}

        n = model.n
        d = model.counts

        # self.probs
        for (g, _) in d.items():
            if len(g) == n:
                self.probs[g[:-1]][g[-1]] = model.cond_prob(g[-1], list(g[:-1]))

        # self.sorted_probs
        self.sorted_probs = self.probs.copy()
        for (x, y) in self.sorted_probs.items():
            l = list(y.items())
            l.sort(key=lambda x: ((-1) * x[1], x[0]))
            self.sorted_probs[x] = l

    def generate_sent(self):
        """Randomly generate a sentence."""
        n = self.n
        sentence = []
        token = ""
        prev_tokens = ('<s>',) * (n-1)
        while 1:
            token = self.generate_token(prev_tokens)
            if token == '</s>':
                break
            sentence.append(token)
            prev_tokens = (prev_tokens + (token,))[1:]
        return sentence

    def generate_token(self, prev_tokens=None):
        """Randomly generate a token, given prev_tokens.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = ()
        assert len(prev_tokens) == n-1

        sorted_probs = self.sorted_probs[tuple(prev_tokens)]
        x = 0
        u = random.random()
        F = sorted_probs[x][1]
        while u > F:
            x += 1
            F += sorted_probs[x][1]
        return sorted_probs[x][0]
