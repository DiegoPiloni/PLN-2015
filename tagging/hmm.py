from math import log2
from collections import defaultdict

class HMM:

    def __init__(self, n, tagset, trans, out):
        """
        n -- n-gram size.
        tagset -- set of tags.
        trans -- transition probabilities dictionary.
        out -- output probabilities dictionary.
        """
        self.n = n
        self.tgset = tagset
        self.trans = trans
        self.out = out

    def tagset(self):
        """Returns the set of tags.
        """
        return self.tgset

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        if prev_tags in self.trans:
            if tag in self.trans[prev_tags]:
                return self.trans[prev_tags][tag]
        return 0

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        if tag in self.out:
            if word in self.out[tag]:
                return self.out[tag][word]
        return 0

    def tag_prob(self, y):
        """
        Probability of a tagging.
        Warning: subject to underflow problems.

        y -- list of tagging.
        """
        n = self.n
        start = ["<s>"] * (n-1)
        stop = ["</s>"]
        y = start + y + stop
        tag_prob = 1
        for i in range(n-1, len(y)):
            tag_prob *= self.trans_prob(y[i], tuple(y[i - n + 1:i]))
            if tag_prob == 0:
                break
        return tag_prob

    def prob(self, x, y):
        """
        Joint probability of a sentence and its tagging.
        Warning: subject to underflow problems.

        x -- sentence.
        y -- tagging.
        """
        len_sent = len(x)
        len_tagging = len(y)
        assert len_sent == len_tagging

        tag_prob = self.tag_prob(y)
        prod_out_prob = 1  # productory of all out probs
        for i in range(len_sent):
            prod_out_prob *= self.out_prob(x[i], y[i])
            if prod_out_prob == 0:
                break
        prob = tag_prob * prod_out_prob
        return prob

    def tag_log_prob(self, y):
        """
        Log-probability of a tagging.

        y -- tagging.
        """
        n = self.n
        start = ["<s>"] * (n-1)
        stop = ["</s>"]
        y = start + y + stop
        tag_log_prob = 0
        for i in range(n-1, len(y)):
            trans_prob = self.trans_prob(y[i], tuple(y[i - n + 1:i]))
            if trans_prob != 0:
                tag_log_prob += log2(trans_prob)
            else:
                tag_log_prob = float('-inf')
                break
        return tag_log_prob

    def log_prob(self, x, y):
        """
        Joint log-probability of a sentence and its tagging.

        x -- sentence.
        y -- tagging.
        """
        len_sent = len(x)
        len_tagging = len(y)
        assert len_sent == len_tagging

        tag_log_prob = self.tag_log_prob(y)
        sum_log_out_prob = 0  # sum of each log of out probs
        for i in range(len_sent):
            out_prob = self.out_prob(x[i], y[i])
            if out_prob != 0:
                sum_log_out_prob += log2(out_prob)
            else:
                sum_log_out_prob = float('-inf')
                break
        prob = tag_log_prob + sum_log_out_prob
        return prob

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        viterbi = ViterbiTagger(self)
        tag = viterbi.tag(sent)
        return tag


class ViterbiTagger:

    def __init__(self, hmm):
        """
        hmm -- the HMM.
        """
        self.hmm = hmm
        self._pi = dict()  # will contain pi dict for each sent tagged

    def tag(self, sent):
        """Returns the most probable tagging for a sentence.

        sent -- the sentence.
        """
        hmm = self.hmm
        n = hmm.n  # n-gram model
        tagset = hmm.tagset()
        pi = defaultdict(lambda:defaultdict(lambda: (0,list())))
        m = len(sent)
        start = ("<s>",)
        stop = "</s>"
        pi[0][start * (n-1)] = (log2(1), [])

        for k in range(1, m+1):
            for v in tagset:
                pi_k = float('-inf')
                pi_k_tag = ""
                for t in pi[k-1]:
                    pi_k_1 = (pi[k-1][t][0])
                    pi_k_1_tags = pi[k-1][t][1]
                    trans = hmm.trans_prob(v, t)
                    out = hmm.out_prob(sent[k-1], v)
                    if trans != 0 and out != 0:
                        s = pi_k_1 + log2(trans) + log2(out)
                        if s > pi_k:
                            pi_k = s
                            pi_k_tag = pi_k_1_tags + [v]
                if pi_k != float('-inf'):
                    pi[k][t[1:] + (v,)] = (pi_k, pi_k_tag)
        for i, d in pi.items():
            print (i)
            for t1, t2 in d.items():
                print(t1, t2)

        self._pi = pi
        max_p = float('-inf')
        max_t = tuple()
        for t in pi[m].keys():
            trans_stop = hmm.trans_prob(stop, t)
            if trans_stop != 0:
                p = pi[m][t][0] * log2(trans_stop)
                if p > max_p:
                    max_p = p
                    max_t = t
        tagging = pi[m][max_t][1]
        return tagging


class MLHMM(HMM):
 
    def __init__(self, n, tagged_sents, addone=True):
        """
        n -- order of the model.
        tagged_sents -- training sentences, each one being a list of pairs.
        addone -- whether to use addone smoothing (default: True).
        """
        self.n = n  # HMM
        self.tagged_sents = tagged_sents
        self.addone = addone

        self.trans_counts = defaultdict(int)
        self.tag_counts = defaultdict(int)
        self.out_counts = defaultdict(lambda: defaultdict(int))
        self.trans = defaultdict(lambda: defaultdict(float))  # HMM
        self.out = defaultdict(lambda: defaultdict(float))    # HMM
        self.tgset = set()  # HMM
        self.vocab = set()
        self.len_vocab = 0
        self.len_tgset = 0
        self._train()
        self.out_counts = dict(self.out_counts)
        self.out = dict(self.out)
        self.trans = dict(self.trans)

        # c_tags for eval
        self.c_tags = c_tags = defaultdict(int)
        for sent in tagged_sents:
            for word, tag in sent:
                c_tags[tag] += 1



    def _train(self):
        """Train counts, trans_p, out_p, vocab and tagset"""
        n = self.n
        start = ["<s>"] * (n-1)
        stop = ["</s>"]

        # counts, vocab and tagset
        for sent in self.tagged_sents:
            if sent:
                for word, tag in sent:
                    self.tag_counts[tag] += 1
                    self.out_counts[tag][word] += 1
                    self.vocab.add(word)
                    self.tgset.add(tag)
                tag_sent = list(zip(*sent))[1]
                tag_sent = start + list(tag_sent) + stop
                for i in range(len(tag_sent) - n + 1):
                    n_gram = tuple(tag_sent[i:i+n])
                    self.trans_counts[n_gram] += 1
                    self.trans_counts[n_gram[:-1]] += 1
        self.len_vocab = len(self.vocab)
        self.len_tgset = len(self.tgset) + 1  # + '</s'>

        # probs
        for tag, word_counts in self.out_counts.items():
            for word, wc in word_counts.items():
                self.out[tag][word] = wc / self.tag_counts[tag]

        for n_gram in self.trans_counts:
            if (len(n_gram)) == n:
                n_gram_count = self.trans_counts[n_gram]
                n_1_gram_count = self.trans_counts[n_gram[:-1]]
                if not self.addone:
                    self.trans[n_gram[:-1]][n_gram[-1]] = n_gram_count / n_1_gram_count
                else:
                    vt = self.len_tgset
                    trans = (n_gram_count + 1) / (n_1_gram_count + vt)
                    self.trans[n_gram[:-1]][n_gram[-1]] = trans

    def tcount(self, tokens):
        """Count for a k-gram for k <= n.
 
        tokens -- the k-gram tuple.
        """
        tcount = 0
        if tokens in self.trans_counts:
            tcount = self.trans_counts[tokens]
        return tcount
 
    def unknown(self, w):
        """Check if a word is unknown for the model.
 
        w -- the word.
        """
        unknown = True
        if w in self.vocab:
            unknown = False
        return unknown

    """
       Todos los métodos de HMM.
    """

    def trans_prob(self, tag, prev_tags):
        """Probability of a tag.

        tag -- the tag.
        prev_tags -- tuple with the previous n-1 tags (optional only if n = 1).
        """
        if prev_tags in self.trans:
            if tag in self.trans[prev_tags]:
                return self.trans[prev_tags][tag]
        if self.addone:
            return (1 / self.len_tgset)
        return 0

    def out_prob(self, word, tag):
        """Probability of a word given a tag.

        word -- the word.
        tag -- the tag.
        """
        out_p = 0
        if word in self.out[tag]:
            out_p = self.out[tag][word]
        else:
            if self.addone:
                out_p = 1 / self.len_vocab
        return out_p