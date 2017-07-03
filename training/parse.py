import re
import collections
import math
import nltk
from nltk.stem.lancaster import LancasterStemmer
import training_data

stemmer = LancasterStemmer()
data = training_data.data


def tokenize(message):
    message = message.lower()
    words_arr = re.findall("[a-z0-9']+", message)
    return set(words_arr)


def count_words(data_set, class_template):
    corpus_words = collections.defaultdict(lambda: class_template.copy())
    for data in data_set:
        for word in tokenize(data['text']):
            stemmed_word = stemmer.stem(word)
            corpus_words[stemmed_word]['_total'] += 1
            corpus_words[stemmed_word][data['class']] += 1
            # class_words[data['class']].append(stemmed_word)
    return corpus_words


def word_probabilities(counts, class_count, class_word, total, k=0.5):
    return [(w, (counts[w][class_word] + k) /
             (class_count[class_word] + 2 * k),
             (counts[w]['_total'] - counts[w][class_word] + k) /
             (total - class_count[class_word] + 2 * k))
            for w in counts]


def class_probability(word_probs, message):
    message_words = tokenize(message)
    log_prob_if_class = log_prob_if_not = 0.0
    for word, prob_if_class, prob_if_not in word_probs:
        if word in message_words:
            log_prob_if_class += math.log(prob_if_class)
            log_prob_if_not += math.log(prob_if_not)
        else:
            log_prob_if_class += math.log(1.0 - prob_if_class)
            log_prob_if_not += math.log(1.0 - prob_if_not)
    prob_if_class = math.exp(log_prob_if_class)
    prob_if_not = math.exp(log_prob_if_not)
    return prob_if_class / (prob_if_class + prob_if_not)


class NaiveBayesClassifier:
    def __init__(self, k=0.5):
        self.k = k
        self.word_probs = {}

    def train(self, data):
        total_num_data = len(data)
        self.class_set = set(a['class'] for a in data)
        # counter with _total key:
        counter = self.class_set.copy()
        counter.add('_total')
        # provides template for corpus
        class_template = dict.fromkeys(counter, 0)
        self.corpus_words = count_words(data, class_template)
        class_count = dict.fromkeys(self.class_set, 0)
        for a in data:
            class_count[a['class']] += 1
        # # keeps track of all words:
        # class_words = collections.defaultdict(lambda: [])
        for klass in self.class_set:
            self.word_probs[klass] = word_probabilities(self.corpus_words,
                                                        class_count, klass,
                                                        total_num_data, self.k)

    def get_probs(self, message):
        for klass in self.class_set:
            print(f"{klass} probability:",
                  class_probability(self.word_probs[klass], message))


if __name__ == "__main__":
    nb = NaiveBayesClassifier()
    nb.train(data)
    nb.get_probs("testing testing one two three")
