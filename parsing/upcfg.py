from collections import defaultdict
from nltk.grammar import Nonterminal as N, PCFG, ProbabilisticProduction
from nltk.tree import Tree
from .cky_parser import CKYParser, NotInLangError
from .util import unlexicalize, lexicalize


class UPCFG:
    """Unlexicalized PCFG.
    """

    def __init__(self, parsed_sents, start='sentence'):
        """
        parsed_sents -- list of training trees.
        """
        self._start = N(start)

        uparsed_sents = [unlexicalize(t.copy(deep=True)) for t in parsed_sents]

        self._productions_counts = pcounts = defaultdict(int)
        self.lhs_counts = lhs_counts = defaultdict(int)

        for t in uparsed_sents:
            t.chomsky_normal_form()
            t.collapse_unary(collapsePOS=True, collapseRoot=True)
            for prod in t.productions():
                pcounts[prod] += 1
                lhs_counts[prod.lhs()] += 1

        self._productions = [ProbabilisticProduction(p.lhs(), p.rhs(),
                             prob=pcounts[p]/lhs_counts[p.lhs()])
                             for p in pcounts]

        pcfg = PCFG(self._start, self._productions)
        self.parser = CKYParser(pcfg)

    def productions(self):
        """Returns the list of UPCFG probabilistic productions.
        """
        return self._productions

    def parse(self, tagged_sent):
        """Parse a tagged sentence.

        tagged_sent -- the tagged sentence (a list of pairs (word, tag)).
        """
        sent, tags = zip(*tagged_sent)
        start = self._start.symbol()
        try:
            parsed_sent = self.parser.parse(tags)[1]
            parsed_sent = lexicalize(parsed_sent, sent)
            parsed_sent.un_chomsky_normal_form()
        except NotInLangError:
            parsed_sent = Tree(start, [Tree(t, [w]) for w, t in tagged_sent])
        return parsed_sent
