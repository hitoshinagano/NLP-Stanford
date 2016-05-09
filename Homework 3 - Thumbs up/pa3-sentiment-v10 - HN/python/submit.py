import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders

from shared_submit import Submitter

from NaiveBayes import NaiveBayes

class NaiveBayesSubmitter(Submitter):
  def validParts(self):
    """Returns a list of valid part names."""

    partNames = [ 'Development All Words', \
                  'Testing All Words', \
                  'Development Without Stop Words', \
                  'Testing Without Stop Words', \
                  'Binarized (Boolean feature) Naive Bayes - Development', \
                  'Binarized (Boolean feature) Naive Bayes - Testing.', \
                  'Best Model - Development', \
                  'Best Model - Test'
                ]
    return partNames


  def sources(self):
    """Returns source files, separated by part. Each part has a list of files."""
    srcs = [ [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ], \
             [ 'NaiveBayes.py' ]
           ]
    return srcs

  def homework_id(self):
    """Returns the string homework id."""
    return '3'



  def output(self, partId, ch_aux):
    """Uses the student code to compute the output for test cases."""
    trainDir = '../data/imdb1/'

    classifier = NaiveBayes()
    if partId == 1: # development on all words
      splits = classifier.crossValidationSplits(trainDir)
      accuracy = 0.0
      for split in splits:
        nb = NaiveBayes()
        nb.train(split)
        guesses = nb.test(split)
        numCorrect = 0.0
        for i in range(0, len(guesses)):
          guess = guesses[i]
          gold = split.test[i].klass
          if guess == gold:
            numCorrect += 1
        accuracy += numCorrect/len(guesses)
      accuracy = accuracy / 10.0
      output = 'accuracy: 1 %f' % accuracy
      return output
    elif partId == 2: # testing on all words
      trainSplit = classifier.trainSplit(trainDir)
      classifier.train(trainSplit)
      testSplit = buildTestCorpus(ch_aux)
      guesses = classifier.test(testSplit)
      guesses.insert(0, '2')
      output = '\n'.join(guesses)
      return output
    elif partId == 3:  # development without stopwords
      splits = classifier.crossValidationSplits(trainDir)
      accuracy = 0.0
      for split in splits:
        nb = NaiveBayes()
        nb.FILTER_STOP_WORDS = True
        nb.train(split)
        guesses = nb.test(split)
        numCorrect = 0.0
        for i in range(0, len(guesses)):
          guess = guesses[i]
          gold = split.test[i].klass
          if guess == gold:
            numCorrect += 1
        accuracy += numCorrect/len(guesses)
      accuracy = accuracy / 10.0
      output = 'accuracy: 3 %f' % accuracy
      return output
    elif partId == 4: # testing without stopwords
      classifier.FILTER_STOP_WORDS = True
      trainSplit = classifier.trainSplit(trainDir)
      classifier.train(trainSplit)
      testSplit = buildTestCorpus(ch_aux)
      guesses = classifier.test(testSplit)
      guesses.insert(0, '4') # put in the part id.
      output = '\n'.join(guesses)
      return output


    elif partId == 5:  # development binarized
      splits = classifier.crossValidationSplits(trainDir)
      accuracy = 0.0
      for split in splits:
        nb = NaiveBayes()
        nb.BOOLEAN_NB = True
        nb.train(split)
        guesses = nb.test(split)
        numCorrect = 0.0
        for i in range(0, len(guesses)):
          guess = guesses[i]
          gold = split.test[i].klass
          if guess == gold:
            numCorrect += 1
        accuracy += numCorrect/len(guesses)
      accuracy = accuracy / 10.0
      output = 'accuracy: 5 %f' % accuracy
      return output
    elif partId == 6: # testing binarized
      classifier.BOOLEAN_NB = True
      trainSplit = classifier.trainSplit(trainDir)
      classifier.train(trainSplit)
      testSplit = buildTestCorpus(ch_aux)
      guesses = classifier.test(testSplit)
      guesses.insert(0, '6') # put in the part id.
      output = '\n'.join(guesses)
      return output

    elif partId == 7:  # development best model
      splits = classifier.crossValidationSplits(trainDir)
      accuracy = 0.0
      for split in splits:
        nb = NaiveBayes()
        nb.BEST_MODEL = True
        nb.train(split)
        guesses = nb.test(split)
        numCorrect = 0.0
        for i in range(0, len(guesses)):
          guess = guesses[i]
          gold = split.test[i].klass
          if guess == gold:
            numCorrect += 1
        accuracy += numCorrect/len(guesses)
      accuracy = accuracy / 10.0
      output = 'accuracy: 7 %f' % accuracy
      return output
    elif partId == 8: # testing best model
      classifier.BEST_MODEL = True
      trainSplit = classifier.trainSplit(trainDir)
      classifier.train(trainSplit)
      testSplit = buildTestCorpus(ch_aux)
      guesses = classifier.test(testSplit)
      guesses.insert(0, '8') # put in the part id.
      output = '\n'.join(guesses)
      return output

    else:
      print 'Unknown partId: %d' % partId
      return None

def buildTestCorpus(ch_aux):
  """takes doc1\n###\ndoc2\n###... and makes list of documents.
     build their NB, train on train, output pos\nneg\npos...
  """
  # split on ###
  testSplit = NaiveBayes.TrainSplit()
  documents = ch_aux.split('###')
  for document in documents:
    document = document.strip() # remove trailing/starting newlines
    example = NaiveBayes.Example() # example for this document
    example.klass = 'UNK' # testing time, we don't know the label
    example.words = []
    for word in document.split(): # for every token
      example.words.append(word)
    testSplit.test.append(example)
  return testSplit

submitter = NaiveBayesSubmitter()
submitter.submit(0)
