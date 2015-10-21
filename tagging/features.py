from collections import namedtuple

from featureforge.feature import Feature


# sent -- the whole sentence.
# prev_tags -- a tuple with the n previous tags.
# i -- the position to be tagged.
History = namedtuple('History', 'sent prev_tags i')


def word_lower(h):
    """Feature: current lowercased word.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].lower()


def word_istitle(h):
    """Feature: current word starts with uppercase letter.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].istitle()


def word_isupper(h):
    """Feature: current word is upper.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isupper()


def word_isdigit(h):
    """Feature: current word is a number.

    h -- a history.
    """
    sent, i = h.sent, h.i
    return sent[i].isdigit()


def prev_tags(h):
    """Feature: previous tags tuple.

    h -- a history.
    """
    prev_tags = h.prev_tags
    return prev_tags


class NPrevTags(Feature):

    def __init__(self, n):
        """Feature: n previous tags tuple.

        n -- number of previous tags to consider.
        """
        self.n = n
        self._name = "{} prev tags".format(n)

    def _evaluate(self, h):
        """n previous tags tuple.

        h -- a history.
        """
        n = self.n
        prev_tags = h.prev_tags
        return prev_tags[-n:]


class PrevWord(Feature):

    def __init__(self, f):
        """Feature: the feature f applied to the previous word.

        f -- the feature.
        """
        self.f = f
        self._name = "Feature to prev. word"

    def _evaluate(self, h):
        """Apply the feature to the previous word in the history.

        h -- the history.
        """
        f = self.f
        sent, prev_tags, i = h.sent, h.prev_tags, h.i
        if i == 0:
            return 'BOS'
        else:
            h1 = History(sent, prev_tags, i - 1)
            return str(f(h1))
