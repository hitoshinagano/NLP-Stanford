import math, collections

class CustomLanguageModel2:
  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.bigramCounts = collections.defaultdict(lambda: 0)
    self.LaplaceUnigramCounts = collections.defaultdict(lambda: 0)
    self.unigramTotal = 0
    self.lda = 0.4  # lambda
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model.
        Compute any counts or other corpus statistics in this function.
    """
    # TODO your code here
    for sentence in corpus.corpus:
      for datum in sentence.data:
        word = datum.word
        if word == '<s>':
          previousWord = '<s>'
          continue
        self.bigramCounts[(previousWord, word)] += 1
        self.LaplaceUnigramCounts[previousWord] += 1
        self.unigramTotal += 1
        previousWord = word

    # adds one to all tokens
    # self.BigramCounts = {k: self.BigramCounts[k] + 1 for k in self.BigramCounts}

    # adds V (vocabulary size) to each unigram count
    # V = len(self.unigramCounts)
    # self.unigramCounts = {k: self.unigramCounts[k] + V for k in self.unigramCounts}

    # adds UNK with zero count
    self.LaplaceUnigramCounts['UNK'] = 0
    # adds one to all tokens
    self.LaplaceUnigramCounts = {k: self.LaplaceUnigramCounts[k] + 1 for k in self.LaplaceUnigramCounts}
    # adds V (vocabulary size) to total words
    self.unigramTotal += len(self.LaplaceUnigramCounts)

    # converting a collections.defaultdict to a normal dict
    # in score, a non-existing key needs to return false, but
    # in a defaultdict, it returns true after the key is called
    # self.bigramCounts = {k: self.bigramCounts[k] for k in self.bigramCounts}

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0

    for word in sentence:
      if word == '<s>':
        previousWord = '<s>'
        continue
      if word not in self.LaplaceUnigramCounts:
        word = 'UNK'
      if (previousWord, word) in self.bigramCounts:
        count = self.bigramCounts[(previousWord, word)]
        score += math.log(count)
        score -= math.log(self.LaplaceUnigramCounts[previousWord])
      else:
        count = self.LaplaceUnigramCounts[word]
        score += math.log(self.lda * count)
        score -= math.log(self.unigramTotal)

      if word != 'UNK':
        score += math.log(len(previousWord))
      previousWord = word

    return score