from collections import defaultdict


class BaselineTagger:

    def __init__(self, tagged_sents):
        """
        tagged_sents -- training sentences, each one being a list of pairs.
        """

        # Tags for each word with counts
        words_tags_counted = defaultdict(lambda: defaultdict(int))
        for sent in tagged_sents:
            for word, tag in sent:
                words_tags_counted[word][tag] += 1

        # Best tag for each word
        self.words_tags = defaultdict(str)
        for w in words_tags_counted:
            c_tags = words_tags_counted[w]
            self.words_tags[w] = max(c_tags.keys(), key=lambda x: c_tags[x])

        # Most frequent tag in tagged_sents
        self.tag_counts = tag_counts = defaultdict(int)
        for sent in tagged_sents:
            for word, tag in sent:
                tag_counts[tag] += 1
        tck = tag_counts.keys()
        self.most_frequent_tag = max(tck, key=lambda x: tag_counts[x])

    def tag(self, sent):
        """Tag a sentence.

        sent -- the sentence.
        """
        return [self.tag_word(w) for w in sent]

    def tag_word(self, w):
        """Tag a word.

        w -- the word.
        """
        unknown = self.unknown(w)
        if unknown:
            tag = self.most_frequent_tag
        else:
            tag = self.words_tags[w]
        return tag

    def unknown(self, w):
        """Check if a word is unknown for the model.

        w -- the word.
        """
        unknown = True
        tagged_words = self.words_tags
        if w in tagged_words:
            unknown = False
        return unknown
