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
        n = self.n
        new_sent = ['<s>']*(n-1) + sent + ['</s>']
        p = 0
        for i in range(n-1, len(new_sent)):
            cond_p = self.cond_prob(new_sent[i], new_sent[i-n+1:i])
            if cond_p == 0:
                p = float('-inf')
                break
            p += log(cond_p, 2)
        return p

    def cross_entropy(self, sents):
        """ Cross-entropy of the model.
        sents -- the test sentences as a list of tokens.
        """
        M = 0  # num of words in test-data.
        for sent in sents:
            M += len(sent)
        l = 0
        for sent in sents:
            l += self.sent_log_prob(sent)
        return (-l/M)

    def perplexity(self, sents):
        """ Perplexity of the model.
        sents -- the test sentences as a list of tokens
        """
        c_ent = self.cross_entropy(sents)
        return 2 ** c_ent


class AddOneNGram(NGram):

    def __init__(self, n, sents):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        """
        super(AddOneNGram, self).__init__(n, sents)
        vocab = []
        for g in self.counts.keys():
            vocab += [w for w in g if w != '<s>']
        self.len_vocab = len(set(vocab))

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
        """Size of the vocabulary."""
        return self.len_vocab


class InterpolatedNGram(NGram):

    def __init__(self, n, sents, gamma=None, addone=True):
        """
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        gamma -- interpolation hyper-parameter (if not given, estimate using
            held-out data).
        addone -- whether to use addone smoothing (default: True).
        """
        assert n > 0
        self.n = n
        self.counts = counts = []
        self.addone = addone
        self.len_vocab = 0

        # n+1 dict of counts
        for _ in range(n+1):
            counts.append(defaultdict(int))

        if not gamma:
            held_out_sents = sents[int(90*len(sents)/100):]
            sents = sents[:int(90*len(sents)/100)]

        self.train_counts(sents, counts)

        if addone:
            vocab = []
            for g in counts[n].keys():  # counts[n] = n-grams
                vocab += [w for w in g if w != '<s>']
            self.vocab = list(set(vocab))
            self.len_vocab = len(self.vocab)

        if gamma:
            self.gamma = gamma
        else:
            num_words = 0
            for sent in held_out_sents:
                num_words += len(sent)
            self.gamma = self.best_gamma(held_out_sents, num_words)

    def train_counts(self, sents, counts):
        n = self.n
        for j in range(1, n+1):
            start = ['<s>'] * (j-1)
            for sent in sents:
                sent = start + sent + ['</s>']
                if j != 1:
                    counts[j-1][tuple(start)] += 1
                for i in range(len(sent) - j + 1):
                    ngram = tuple(sent[i: i + j])
                    counts[j][ngram] += 1
                    if j == 1:
                        counts[j-1][ngram[:-1]] += 1

    def count(self, tokens):
        """Count for an n-gram or (n-1)-gram in the training data.
        tokens -- the n-gram or (n-1)-gram tuple.
        """
        n = len(tokens)
        return self.counts[n][tokens]

    def best_gamma(self, held_out_sents, M):
        """Find best gamma as argmax of perplexity.
        M -- number of words in held_out_sents
        """
        self.gamma = 1
        best_gamma = self.gamma
        actual_perp = self.perplexity(held_out_sents, M)
        best_perp = actual_perp
        self.gamma = 0
        for _ in range(20):
            self.gamma += 100
            actual_perp = self.perplexity(held_out_sents, M)
            if actual_perp < best_perp:
                best_perp = actual_perp
                best_gamma = self.gamma
        return best_gamma

    def lambdas(self, tokens):
        """List of lambdas for n-gram interpolated model
        tokens -- (n-1)-gram tuple.
        """
        n = self.n
        gamma = self.gamma
        assert len(tokens) == n-1
        lambdas = []
        if n == 1:
            lambdas.append(1)
        else:
            for i in range(n-1):
                c = self.count(tokens[i:])
                l_i = (1 - sum(lambdas)) * (c / (c + gamma))
                lambdas.append(l_i)
            lambdas.append(1-sum(lambdas))
        return lambdas

    def cond_prob_ML(self, token, prev_tokens=None):
        """Maximum Likelihood conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        addone = self.addone
        if not prev_tokens:
            prev_tokens = []
        tokens = prev_tokens + [token]
        count_ngram = float(self.count(tuple(tokens)))
        count_n_1gram = self.count(tuple(prev_tokens))
        if addone:
            c_p = (count_ngram + 1) / (count_n_1gram + self.V())
        else:
            c_p = count_ngram / count_n_1gram
        return c_p

    def cond_prob(self, token, prev_tokens=None):
        """Linear interpolated conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        n = self.n
        if not prev_tokens:
            prev_tokens = []
        assert len(prev_tokens) == n-1
        lambdas = self.lambdas(tuple(prev_tokens))
        cp_LI = 0
        for i in range(n):
            lambd_i = lambdas[i]
            if lambd_i != 0:
                cp_LI += self.cond_prob_ML(token, prev_tokens[i:]) * lambd_i
        return cp_LI

    def V(self):
        """Size of the vocabulary."""
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
