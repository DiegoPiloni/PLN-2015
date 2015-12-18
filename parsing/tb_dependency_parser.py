from featureforge.vectorizer import Vectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from parsing.features import (History, distance, top_pos, top_word, TopNWordsOfStack,
                              TopNPosOfStack, TopNWordsOfBuf, TopNPosOfBuf)


class TBDependencyParser():

    def __init__(self, parsed_sents, classifier='svm'):
        """
        parsed_sents -- list of sentences (each one a list of lists ::
                        [[Word, Root, Pos, Head]]
        classifier -- classifier to be used in the sklearn pipeline.
        """
        self.parsed_sents = parsed_sents

        # Posible classifiers
        classifiers = {'lr': LogisticRegression(),
                       'svm': LinearSVC()}

        # Features

        self.features = [distance, top_pos, top_word]
        n = 2  # Best Accuracy found
        self.features += [TopNWordsOfStack(i) for i in range(1, n+1)]
        self.features += [TopNPosOfStack(i) for i in range(1, n+1)]
        self.features += [TopNWordsOfBuf(i) for i in range(1, n+1)]
        self.features += [TopNPosOfBuf(i) for i in range(1, n+1)]

        # Pipeline for tag classifier
        self.action_clf = Pipeline([('vect', Vectorizer(self.features)),
                                    ('clf', classifiers[classifier]),
                                    ])

        sents_histories, sents_actions = self.sents_histories_actions(parsed_sents)

        self.action_clf = self.action_clf.fit(sents_histories, sents_actions)

    def sents_histories_actions(self, parsed_sents):
        """
        Returns tuple (histories, actions) of a corpus.
        parsed_sents -- the corpus (a list of sentences)
        """
        sents_histories = []
        sents_actions = []
        for ps in parsed_sents:
            ps_histories, ps_actions = self.sent_histories_actions(ps)
            sents_histories += ps_histories
            sents_actions += ps_actions
        return (sents_histories, sents_actions)

    def sent_histories_actions(self, parsed_sent):
        """
        Returns tuple (histories, actions) of a parsed sentence.
        parsed_sent -- the parsed sentence (a list of lists ::
                       [word, root, postag, head]).
        """
        ROOT = ["0", "ROOT", "ROOT", "ROOT", "-1"]
        complete_stack = [ROOT]
        hist_stack = [[ROOT[0], ROOT[1], ROOT[3]]]
        complete_buf = [[str(i+1)] + l for i, l in enumerate(parsed_sent)]
        hist_buf = [[l[0], l[1], l[3]] for l in complete_buf]
        hs = list()
        actions = list()

        while hist_buf:
            if len(hist_stack) > 1:
                if complete_buf[0][4] == complete_stack[-1][0]:
                    hs.append(History(hist_stack, hist_buf))
                    actions.append("RIGHT ARC")
                    top_of_hist_buf = hist_buf[0]
                    top_of_complete_buf = complete_buf[0]
                    hist_buf = hist_buf[1:]
                    complete_buf = complete_buf[1:]
                    hist_stack = hist_stack + [top_of_hist_buf]
                    complete_stack = complete_stack + [top_of_complete_buf]
                elif complete_stack[-1][4] == complete_buf[0][0]:
                    hs.append(History(hist_stack, hist_buf))
                    actions.append("LEFT ARC")
                    hist_stack = hist_stack[:-1]
                    complete_stack = complete_stack[:-1]
                else:  # Not related
                    # check if any of the stack elem is related with top of buf
                    some_of_stack_related = False
                    for elem in complete_stack:
                        if elem[4] == complete_buf[0][0] or complete_buf[0][4] == elem[0]:
                            some_of_stack_related = True
                            break
                    if some_of_stack_related:
                        hs.append(History(hist_stack, hist_buf))
                        actions.append("REDUCE")
                        hist_stack = hist_stack[:-1]
                        complete_stack = complete_stack[:-1]
                    else:
                        hs.append(History(hist_stack, hist_buf))
                        actions.append("SHIFT")
                        top_of_hist_buf = hist_buf[0]
                        top_of_complete_buf = complete_buf[0]
                        hist_buf = hist_buf[1:]
                        complete_buf = complete_buf[1:]
                        hist_stack = hist_stack + [top_of_hist_buf]
                        complete_stack = complete_stack + [top_of_complete_buf]
            else:
                hs.append(History(hist_stack, hist_buf))
                actions.append("SHIFT")
                top_of_hist_buf = hist_buf[0]
                top_of_complete_buf = complete_buf[0]
                hist_buf = hist_buf[1:]
                complete_buf = complete_buf[1:]
                hist_stack = hist_stack + [top_of_hist_buf]
                complete_stack = complete_stack + [top_of_complete_buf]

        return (hs, actions)

    def actions(self, sent):
        """Chooce actions for a sentence.
        sent -- the sentence.
        """
        actions = list()
        stack = [["0", "ROOT", "ROOT"]]
        sent = [[str(i+1)] + list(l) for i, l in enumerate(sent)]
        buf = sent

        while buf and stack:
            hi = History(stack, buf)
            action = self.action_history(hi)
            actions.append(action)
            if action == "SHIFT" or action == "RIGHT ARC":
                top_of_buf = buf[0]
                buf = buf[1:]
                stack = stack + [top_of_buf]
            elif action == "LEFT ARC" or action == "REDUCE":
                stack = stack[:-1]

        return actions

    def action_history(self, h):
        """Predict an action for a history.
        h -- the history.
        """
        predicted_action = self.action_clf.predict([h])[0]
        return predicted_action
