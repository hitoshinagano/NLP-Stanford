import math, collections

class LaplaceUnigramLanguageModel:

  def __init__(self, corpus):
    """Initialize your data structures in the constructor."""
    self.LaplaceUnigramCounts = collections.defaultdict(lambda: 0)
    self.total = 0
    self.train(corpus)

  def train(self, corpus):
    """ Takes a corpus and trains your language model. 
        Compute any counts or other corpus statistics in this function.
    """  
    # TODO your code here
    # Tip: To get words from the corpus, try
    #    for sentence in corpus.corpus:
    #       for datum in sentence.data:
    #         word = datum.word

    for sentence in corpus.corpus:
      for datum in sentence.data:
        word = datum.word
        self.LaplaceUnigramCounts[word] += 1    # defaultdict funciona bem aqui: nao da' keyerror
        self.total += 1

    # adds UNK with zero count
    self.LaplaceUnigramCounts['UNK'] = 0
    # adds one to all tokens
    self.LaplaceUnigramCounts = {k: self.LaplaceUnigramCounts[k] + 1 for k in self.LaplaceUnigramCounts}
    # adds V (vocabulary size) to total words
    self.total += len(self.LaplaceUnigramCounts)

    #pass

  def score(self, sentence):
    """ Takes a list of strings as argument and returns the log-probability of the 
        sentence using your language model. Use whatever data you computed in train() here.
    """
    # TODO your code here
    score = 0.0

    for token in sentence:
      if token not in self.LaplaceUnigramCounts: token = 'UNK'
      count = self.LaplaceUnigramCounts[token]
      if count > 0:
        score += math.log(count)
        score -= math.log(self.total)

    return score
