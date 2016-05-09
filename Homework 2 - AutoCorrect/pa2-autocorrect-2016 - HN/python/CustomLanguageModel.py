import math, collections

class CustomLanguageModel:


  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.LaplaceBigramCounts = collections.defaultdict(lambda: 0)
    self.unigramCounts = collections.defaultdict(lambda: 0)
    self.bigramTotal = 0
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
        self.LaplaceBigramCounts[(previousWord, word)] += 1
        self.unigramCounts[previousWord] += 1
        self.bigramTotal += 1
        previousWord = word
    # pass


    # 'UNK' token to account for words not learned in train that show up in test
    self.unigramCounts['UNK'] = 0

    # create entries for bigrams not found, for words in the vocabulary
    wordSet = self.unigramCounts.keys()
    for w1 in wordSet:
      for w2 in wordSet:
        if (w1, w2) not in self.LaplaceBigramCounts:
          self.LaplaceBigramCounts[(w1, w2)] = 0

    # remove ('UNK', '<s>')
    # remove ('<\s>', 'UNK')
    self.LaplaceBigramCounts.pop(('UNK', '<s>'))
    # self.LaplaceBigramCounts.pop(('<\s>', 'UNK'))

    # adds one to all tokens
    self.LaplaceBigramCounts = {k: self.LaplaceBigramCounts[k] + 1 for k in self.LaplaceBigramCounts}

    # adds V (vocabulary size) to each unigram count
    V = len(self.unigramCounts)
    self.unigramCounts = {k: self.unigramCounts[k] + V for k in self.unigramCounts}


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
      if word not in self.unigramCounts: word = 'UNK'
      count = self.LaplaceBigramCounts[(previousWord, word)]

      score += math.log(count)
      score -= math.log(self.unigramCounts[previousWord])
      if word != 'UNK':
        score += math.log(len(previousWord))
      previousWord = word

    return score
