from collections import namedtuple

from featureforge.feature import Feature

# stack -- The stack with words analized but maybe not fully related.
# buffer -- Words not analized yet.
History = namedtuple('History', 'stack buffer')


def distance(h):
    """Feature: distance in sentence from last of stack and top of buffer.

    h -- a history."""
    stack, buf = h.stack, h.buffer
    i_buf = buf[0][0]
    i_stack = 0
    if stack:
        i_stack = stack[-1][0]
    return int(i_buf) - int(i_stack)


def top_word(h):
    """Feature: pair(top_of_stack_word, top_of_buffer_word)

    h -- a history"""
    stack = h.stack
    buf = h.buffer
    if stack:
        return (stack[-1][1], buf[0][1])
    else:
        return (" ", buf[0][1])


def top_pos(h):
    """Feature: pair(top_of_stack_pos, top_of_buffer_pos)

    h -- a history"""
    stack = h.stack
    buf = h.buffer
    if stack:
        return (stack[-1][2], buf[0][2])
    else:
        return (" ", buf[0][2])


class TopNWordsOfStack(Feature):
    def __init__(self, n):
        self.n = n

    def _evaluate(self, h):
        n = self.n
        stack = h.stack
        if stack:
            topn = stack[-n:]
            return [l[1].lower() for l in topn]
        else:
            return []


class TopNPosOfStack(Feature):
    def __init__(self, n):
        self.n = n

    def _evaluate(self, h):
        n = self.n
        stack = h.stack
        if stack:
            topn = stack[-n:]
            return [l[2] for l in topn]
        else:
            return []


class TopNWordsOfBuf(Feature):
    def __init__(self, n):
        self.n = n

    def _evaluate(self, h):
        n = self.n
        buf = h.buffer
        topn = buf[:n]
        return [l[1].lower() for l in topn]


class TopNPosOfBuf(Feature):
    def __init__(self, n):
        self.n = n

    def _evaluate(self, h):
        n = self.n
        buf = h.buffer
        topn = buf[:n]
        return [l[2] for l in topn]
