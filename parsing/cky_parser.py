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
            rhs0 = p.rhs()[0].symbol()
            rhs1 = p.rhs()[1].symbol()
            self._nonlexical_productions[(rhs0, rhs1)].append(p)

        self._pi = defaultdict(dict)  # pi for each (X, i, j)
        self._bp = defaultdict(dict)  # backpointers for each (X, i, j)

    def parse(self, sent):
        """Parse a sequence of terminals.

        sent -- the sequence of terminals.
        """
        n = len(sent)
        start = self._start.symbol()
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
                for s in range(i, j):
                    rhs0 = pi[(i, s)].keys()
                    rhs1 = pi[(s+1, j)].keys()
                    prods = []
                    for r0 in rhs0:
                        for r1 in rhs1:
                            prods += nonlexical_prod[(r0, r1)]
                    for prod in prods:
                        rhs = prod.rhs()
                        x = prod.lhs().symbol()
                        if x not in pi[(i, j)]:
                            pi[(i, j)][x] = float('-inf')
                        y = rhs[0].symbol()
                        z = rhs[1].symbol()
                        q_xyz = prod.logprob()
                        pi_split1 = pi[(i, s)][y]
                        pi_split2 = pi[(s+1, j)][z]
                        pi_xyz_s = q_xyz + pi_split1 + pi_split2
                        if pi_xyz_s > pi[(i, j)][x]:
                            pi[(i, j)][x] = pi_xyz_s
                            ltree = bp[(i, s)][y]
                            rtree = bp[(s+1, j)][z]
                            bp[(i, j)][x] = Tree(x, [ltree, rtree])

        self._pi = pi
        self._bp = bp
        if start in pi[(1, n)]:
            return (pi[(1, n)][start], bp[(1, n)][start])
        else:
            raise NotInLangError(sent)
