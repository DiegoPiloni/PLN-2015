# https://docs.python.org/3/library/collections.html
from collections import defaultdict
from math import log
import random
import sys

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
        return self.counts[tuple(tokens)] / self.counts[tuple(prev_tokens)]

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
        i = 0 # numero de sent
        l_s = len(sents) # numero total de sents
        for sent in sents:
            i += 1
            sys.stdout.write(str(i) + " | " + str(l_s) + "\r")
            sys.stdout.flush()
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

        if gamma is None:
            held_out_sents = sents[int(90*len(sents)/100):]
            sents = sents[:int(90*len(sents)/100)]

        self.train_counts(sents, counts)

        if addone:
            vocab = []
            for g in counts[n].keys():  # counts[n] = n-grams
                vocab += [w for w in g if w != '<s>']
            self.vocab = list(set(vocab))
            self.len_vocab = len(self.vocab)

        if gamma is None:
            self.gamma = self.best_gamma(held_out_sents)
        else:
            self.gamma = gamma

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

    def best_gamma(self, held_out_sents):
        """Find best gamma as argmax of perplexity.
        """
        self.gamma = 1
        best_gamma = self.gamma
        actual_perp = self.perplexity(held_out_sents)
        best_perp = actual_perp
        self.gamma = 0
        for _ in range(20):
            self.gamma += 100
            actual_perp = self.perplexity(held_out_sents)
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
        if addone and len(tokens) == 1:
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


class BackOffNGram(NGram):

    def __init__(self, n, sents, beta=None, addone=True):
        """
        Back-off NGram model with discounting as described by Michael Collins.
        n -- order of the model.
        sents -- list of sentences, each one being a list of tokens.
        beta -- discounting hyper-parameter (if not given, estimate using
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

        if beta is None:
            held_out_sents = sents[int(90*len(sents)/100):]
            sents = sents[:int(90*len(sents)/100)]

        self.train_counts(sents, counts)

        if addone:
            vocab = []
            for g in counts[n].keys():  # counts[n] = n-grams
                vocab += [w for w in g if w != '<s>']
            self.vocab = list(set(vocab))
            self.len_vocab = len(self.vocab)

        self.Asets = defaultdict(set)
        self.train_Asets()

        self.alphas = dict()
        self.denoms = dict()

        if beta is None:
            self.beta = self.best_beta(held_out_sents)
        else:
            self.beta = beta
            self.train_alphas()
            self.train_denoms()

    def train_Asets(self):
        n = self.n
        for i in range(1, n+1):
            for tokens in self.counts[i].keys():
                self.Asets[tokens[:-1]].add(tokens[-1])
                if "<s>" in self.Asets[tokens[:-1]]:
                    self.Asets[tokens[:-1]].remove("<s>")

    def train_alphas(self):
        self.alphas = dict()
        s = 0
        for g in self.Asets.keys():
            s = 0
            c_g = self.count(g)
            for w in self.Asets[g]:
                s += self.star_count(g + (w,)) / c_g
            self.alphas[g] = 1 - s

    def train_denoms(self):
        self.denoms = dict()
        n = self.n
        s = 0
        for i in range(1, n):
            for tokens in self.counts[i].keys():
                s = 0
                for x in self.Asets[tokens]:
                    s += self.cond_prob(x, list(tokens[1:]))
                self.denoms[tokens] = 1 - s

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
        """Count for a k-gram in the training data.
        tokens -- the k-gram tuple.
        """
        n = len(tokens)
        c = 0
        if tokens in self.counts[n]:
            c = self.counts[n][tokens]
        return c

    def star_count(self, tokens):
        """ Count* for Back-off model """
        return self.count(tokens) - self.beta

    def best_beta(self, held_out_sents):
        """Find best beta as argmax of perplexity.
        """
        self.beta = 0.1
        best_beta = self.beta
        best_perp = float('inf')
        actual_perp = best_perp
        for _ in range(9):
            self.train_alphas()
            self.train_denoms()
            actual_perp = self.perplexity(held_out_sents)
            if actual_perp < best_perp:
                best_perp = actual_perp
                best_beta = self.beta
            self.beta += 0.1
        return best_beta

    def cond_prob_ML(self, token, prev_tokens=None):
        """Maximum Likelihood conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        addone = self.addone
        if not prev_tokens:
            prev_tokens = []
        tokens = prev_tokens + [token]
        star_count_ngram = float(self.star_count(tuple(tokens)))
        count_ngram = float(self.count(tuple(tokens)))
        count_n_1gram = self.count(tuple(prev_tokens))
        if len(tokens) == 1:
            if addone:
                c_p = (count_ngram + 1) / (count_n_1gram + self.V())
            else:
                c_p = count_ngram / count_n_1gram
        else:
            c_p = star_count_ngram / count_n_1gram
        return c_p

    def cond_prob(self, token, prev_tokens=None):
        """Linear interpolated conditional probability of a token.
        token -- the token.
        prev_tokens -- the previous n-1 tokens (optional only if n = 1).
        """
        if not prev_tokens:
            prev_tokens = []
        tup_prev = tuple(prev_tokens)
        tokens = tup_prev + (token,)
        A = self.A(tup_prev)
        if token in A:
            cond_p = self.cond_prob_ML(token, prev_tokens)
        else:
            if len(prev_tokens) == 0:  # unigrams
                cond_p = self.cond_prob_ML(token, prev_tokens)
            else:
                c_p = self.cond_prob(token, prev_tokens[1:])
                alpha = self.alpha(tup_prev)
                denom = self.denom(tup_prev)
                cond_p = alpha * c_p / denom
        return cond_p

    def A(self, tokens):
        """Set of words with counts > 0 for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        a = set()
        if tokens in self.Asets:
            a = self.Asets[tokens]
        return a

    def alpha(self, tokens):
        """Missing probability mass for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        a = 1
        if tokens in self.alphas:
            a =  self.alphas[tokens]
        return a

    def denom(self, tokens):
        """Normalization factor for a k-gram with 0 < k < n.
        tokens -- the k-gram tuple.
        """
        d = 1
        if tokens in self.denoms:
            d = self.denoms[tokens]
        return d

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
                prev = list(g[:-1])
                self.probs[g[:-1]][g[-1]] = model.cond_prob(g[-1], prev)

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
