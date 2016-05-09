import math
from Datum import Datum
from Sentence import Sentence
from HolbrookCorpus import HolbrookCorpus
from UniformLanguageModel import UniformLanguageModel
from UnigramLanguageModel import UnigramLanguageModel
from StupidBackoffLanguageModel import StupidBackoffLanguageModel
from LaplaceUnigramLanguageModel import LaplaceUnigramLanguageModel
from LaplaceBigramLanguageModel import LaplaceBigramLanguageModel
from CustomLanguageModel import CustomLanguageModel
from CustomLanguageModel2 import CustomLanguageModel2
from EditModel import EditModel
from SpellingResult import SpellingResult
import types

# Modified version of Peter Norvig's spelling corrector
"""Spelling Corrector.

Copyright 2007 Peter Norvig. 
Open source code under MIT license: http://www.opensource.org/licenses/mit-license.php
"""

import re, collections

class SpellCorrect:
  """Spelling corrector for sentences. Holds edit model, language model and the corpus."""

  def __init__(self, lm, corpus):
    self.languageModel = lm
    self.editModel = EditModel('../data/count_1edit.txt', corpus)

  def correctSentence(self, sentence):
    """Assuming exactly one error per sentence, returns the most probable corrected sentence.
       Sentence is a list of words."""

    if len(sentence) == 0:
      return []

    #bestSentence = sentence[:] #copy of sentence
    trySentence  = sentence[:] #copy of sentence
    bestScore = float('-inf')

    # checking original sentence score: #print self.languageModel.score(bestSentence)

    for i in xrange(1, len(sentence) - 1): #ignore <s> and </s>
      # TODO: select the maximum probability sentence here, according to the noisy channel model.
      # Tip: self.editModel.editProbabilities(word) gives edits and log-probabilities according to your edit model.
      #      You should iterate through these values instead of enumerating all edits.
      # Tip: self.languageModel.score(trialSentence) gives log-probability of a sentence
      # checking contents : # print self.editModel.editProbabilities(sentence[i])
      for w, p in self.editModel.editProbabilities(sentence[i]):
          trySentence[i] = w
          if self.languageModel.score(trySentence) + p > bestScore:   # p : channel model
              bestScore = self.languageModel.score(trySentence) + p   # self.languageModel.score(trySentence) : prior
              bestSentence = trySentence[:]
      trySentence[i] = sentence[i]


      #pass

    # if True: #bestSentence != sentence:
    #     print self.languageModel.score(sentence), ' '.join(sentence)
    #     print self.languageModel.score(bestSentence),' '.join(bestSentence)
    #     print

    return bestSentence

  def evaluate(self, corpus):  
    """Tests this speller on a corpus, returns a SpellingResult"""
    numCorrect = 0
    numTotal = 0
    testData = corpus.generateTestCases()
    for sentence in testData:
      if sentence.isEmpty():
        continue
      errorSentence = sentence.getErrorSentence()
      hypothesis = self.correctSentence(errorSentence)
      if sentence.isCorrection(hypothesis):
        numCorrect += 1
      numTotal += 1
    return SpellingResult(numCorrect, numTotal)

  def correctCorpus(self, corpus): 
    """Corrects a whole corpus, returns a JSON representation of the output."""
    string_list = [] # we will join these with commas,  bookended with []
    sentences = corpus.corpus
    for sentence in sentences:
      uncorrected = sentence.getErrorSentence()
      corrected = self.correctSentence(uncorrected)
      word_list = '["%s"]' % '","'.join(corrected)
      string_list.append(word_list)
    output = '[%s]' % ','.join(string_list)
    return output

def main():
  """Trains all of the language models and tests them on the dev data. Change devPath if you
     wish to do things like test on the training data."""
  trainPath = '../data/holbrook-tagged-train.dat'
  trainingCorpus = HolbrookCorpus(trainPath)

  devPath = '../data/holbrook-tagged-dev.dat'
  devCorpus = HolbrookCorpus(devPath)

  print 'Unigram Language Model: '
  unigramLM = UnigramLanguageModel(trainingCorpus)
  unigramSpell = SpellCorrect(unigramLM, trainingCorpus)
  unigramOutcome = unigramSpell.evaluate(devCorpus)
  print str(unigramOutcome)

  print 'Uniform Language Model: '
  uniformLM = UniformLanguageModel(trainingCorpus)
  uniformSpell = SpellCorrect(uniformLM, trainingCorpus)
  uniformOutcome = uniformSpell.evaluate(devCorpus)
  print str(uniformOutcome)

  print 'Laplace Unigram Language Model: '
  laplaceUnigramLM = LaplaceUnigramLanguageModel(trainingCorpus)
  laplaceUnigramSpell = SpellCorrect(laplaceUnigramLM, trainingCorpus)
  laplaceUnigramOutcome = laplaceUnigramSpell.evaluate(devCorpus)
  print str(laplaceUnigramOutcome)

  print 'Laplace Bigram Language Model: '
  laplaceBigramLM = LaplaceBigramLanguageModel(trainingCorpus)
  laplaceBigramSpell = SpellCorrect(laplaceBigramLM, trainingCorpus)
  laplaceBigramOutcome = laplaceBigramSpell.evaluate(devCorpus)
  print str(laplaceBigramOutcome)

  print 'Stupid Backoff Language Model: '
  sbLM = StupidBackoffLanguageModel(trainingCorpus)
  sbSpell = SpellCorrect(sbLM, trainingCorpus)
  sbOutcome = sbSpell.evaluate(devCorpus)
  print str(sbOutcome)

  print 'Custom Language Model (based on LaplaceBigramLanguageModel): '
  customLM = CustomLanguageModel(trainingCorpus)
  customSpell = SpellCorrect(customLM, trainingCorpus)
  customOutcome = customSpell.evaluate(devCorpus)
  print str(customOutcome)

  print 'Custom Language Model2 (based on StupidBackoffLanguageModel): '
  customLM2 = CustomLanguageModel2(trainingCorpus)
  customSpell2 = SpellCorrect(customLM2, trainingCorpus)
  customOutcome2 = customSpell2.evaluate(devCorpus)
  print str(customOutcome2)

if __name__ == "__main__":
    main()
