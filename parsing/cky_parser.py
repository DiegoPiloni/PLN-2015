from collections import defaultdict
from nltk.tree import Tree


class NotInLangError(Exception):
    def __init__(self, sent):
        self.sent = sent

    def __str__(self):
        return " ".join(self.sent)


class CKYParser:

    def __init__(self, grammar):
        """
        grammar -- a binarised NLTK PCFG.
        """
        self.grammar = grammar
        prods = grammar.productions()
        self._start = grammar.start()  # Represent nonterminal as str

        lexical_productions = [p for p in prods if p.is_lexical()]
        self._lexical_productions = defaultdict(list)
        for p in lexical_productions:
            self._lexical_productions[p.rhs()[0]].append(p)

        nonlexical_productions = [p for p in prods if p.is_nonlexical()]
        self._nonlexical_productions = defaultdict(list)
        for p in nonlexical_productions:
            self._nonlexical_productions[p.lhs()].append(p)

        self._non_terminals = set(p.lhs() for p in prods)
        self._pi = defaultdict(dict)  # pi for each (X, i, j)
        self._bp = defaultdict(dict)  # backpointers for each (X, i, j)

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """
        n = len(sent)
        start = self._start.symbol()
        non_terminals = self._non_terminals
        lexical_prod = self._lexical_productions
        nonlexical_prod = self._nonlexical_productions

        pi = defaultdict(dict)
        bp = defaultdict(dict)

        # Initialize
        for i in range(1, n+1):
            y = sent[i-1]
            for prod in lexical_prod[y]:
                x = prod.lhs().symbol()  # convert it into str
                pi[(i, i)][x] = prod.logprob()
                bp[(i, i)][x] = Tree(x, [y])

        # Algorithm
        for l in range(1, n):
            for i in range(1, n-l+1):
                j = i + l
                for x in non_terminals:
                    # nonlexical productions with lhs x
                    x_prod = nonlexical_prod[x]
                    x = x.symbol()  # str representation
                    pi_ijx = float('-inf')
                    for prod in x_prod:
                        rhs = prod.rhs()
                        y = rhs[0].symbol()
                        z = rhs[1].symbol()
                        q_xyz = prod.logprob()
                        for s in range(i, j):
                            pi_split1 = float('-inf')
                            pi_split2 = float('-inf')
                            if y in pi[(i, s)]:
                                pi_split1 = pi[(i, s)][y]
                            if z in pi[(s+1, j)]:
                                pi_split2 = pi[(s+1, j)][z]
                            pi_xyz_s = q_xyz + pi_split1 + pi_split2
                            if pi_xyz_s > pi_ijx:
                                pi_ijx = pi_xyz_s
                                ltree = bp[(i, s)][y]
                                rtree = bp[(s+1, j)][z]
                    if pi_ijx != float('-inf'):
                        pi[(i, j)][x] = pi_ijx
                        bp[(i, j)][x] = Tree(x, [ltree, rtree])

        self._pi = pi
        self._bp = bp
        if start in pi[(1, n)]:
            return (pi[(1, n)][start], bp[(1, n)][start])
        else:
            raise NotInLangError(sent)
