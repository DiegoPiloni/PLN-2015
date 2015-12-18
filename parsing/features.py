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

def top_of_stack_word(h):
    """Feature: Top of stack word

    h -- a history."""
    stack = h.stack
    if stack:
        return stack[-1][1].lower()
    else:
        return "ES"

def top_of_stack_pos(h):
    """Feature: Top of stack pos

    h -- a history."""
    stack = h.stack
    if stack:
        return stack[-1][2]
    else:
        return "ES"

def top_of_buf_word(h):
    """Feature: Top of buffer word

    h -- a history."""
    buf = h.buffer
    return buf[0][1].lower()

def top_of_buf_pos(h):
    """Feature: Top of buffer word

    h -- a history."""
    buf = h.buffer
    return buf[0][2]
