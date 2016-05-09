import sys
import getopt
import os
import math
from NaiveBayes import Example, TrainSplit


def readFile(fileName):
  """
  * Code for reading a file.  you probably don't want to modify anything here, 
  * unless you don't like the way we segment files.
  """
  contents = []
  f = open(fileName)
  for line in f:
    contents.append(line)
  f.close()
  result = segmentWords('\n'.join(contents)) 
  return result

def segmentWords(s):
  """
   * Splits lines on whitespace for file reading
  """
  return s.split()

def buildSplits(numFolds, args):
  """Builds the splits for training/testing"""
  splits = []
  trainDir = args[0]
  if len(args) == 1: 
    print '[INFO]\tPerforming %d-fold cross-validation on data set:\t%s' % (numFolds, trainDir)
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fold in range(0, numFolds):
      split = TrainSplit()
      for fileName in posTrainFileNames:
        example = Example()
        example.words = readFile('%s/pos/%s' % (trainDir, fileName))
        example.klass = 'pos'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      for fileName in negTrainFileNames:
        example = Example()
        example.words = readFile('%s/neg/%s' % (trainDir, fileName))
        example.klass = 'neg'
        if fileName[2] == str(fold):
          split.test.append(example)
        else:
          split.train.append(example)
      splits.append(split)
  elif len(args) == 2:
    split = TrainSplit()
    testDir = args[1]
    print '[INFO]\tTraining on data set:\t%s testing on data set:\t%s' % (trainDir, testDir)
    posTrainFileNames = os.listdir('%s/pos/' % trainDir)
    negTrainFileNames = os.listdir('%s/neg/' % trainDir)
    for fileName in posTrainFileNames:
      example = Example()
      example.words = readFile('%s/pos/%s' % (trainDir, fileName))
      example.klass = 'pos'
      split.train.append(example)
    for fileName in negTrainFileNames:
      example = Example()
      example.words = readFile('%s/neg/%s' % (trainDir, fileName))
      example.klass = 'neg'
      split.train.append(example)

    posTestFileNames = os.listdir('%s/pos/' % testDir)
    negTestFileNames = os.listdir('%s/neg/' % testDir)
    for fileName in posTestFileNames:
      example = Example()
      example.words = readFile('%s/pos/%s' % (testDir, fileName)) 
      example.klass = 'pos'
      split.test.append(example)
    for fileName in negTestFileNames:
      example = Example()
      example.words = readFile('%s/neg/%s' % (testDir, fileName)) 
      example.klass = 'neg'
      split.test.append(example)
    splits.append(split)
  return splits
  
