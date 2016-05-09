#!/usr/bin/env python

import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import os
import sys

from shared_submit import Submitter

from IRSystem import IRSystem

class IRSubmitter(Submitter):
  def validParts(self):
      """Returns a list of valid part names."""

      partNames = [ 'Inverted Index Dev', \
                    'Inverted Index Test', \
                   'Boolean Retrieval Dev', \
                    'Boolean Retrieval Test', \
                    'Phrase Query Retrieval Dev', \
                    'Phrase Query Retrieval Test', \
                    'TF-IDF Dev', \
                    'TF-IDF Test', \
                    'Cosine Similarity Dev', \
                    'Cosine Similarity Test'
                  ]
      return partNames


  def sources(self):
      """
      Returns source files, separated by part. Each part has a list of files.
      """
      srcs = [ [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'], \
               [ 'IRSystem.py'] \
             ]
      return srcs

  def homework_id(self):
      """Returns the string homework id."""
      return '4'

  def output(self, partId, ch_aux):
      """Uses the student code to compute the output for test cases."""
      version = 1
      output = [partId, version]

      irsys = IRSystem()
      irsys.read_data('../data/RiderHaggard')
      irsys.index()
      irsys.compute_tfidf()

      out = sys.stdout
      if partId in [2,4,6,8,10]:   # test parts
          sys.stdout = open(os.devnull, 'w')

      if partId == 1 or partId == 2:
          # Inverted Index. 1 ==> dev; 2 ==> test
          queries = ch_aux.split(", ")
          for query in queries:
              posting = irsys.get_posting_unstemmed(query)
              output.append(list(posting))
      elif partId == 3 or partId == 4:
          # Boolean Retrieval. 3 ==> dev; 4 ==> test
          queries = ch_aux.split(", ")
          for query in queries:
              result = irsys.query_retrieve(query)
              result = list(result)
              output.append(result)
      elif partId == 5 or partId == 6:
          # Phrase Query Retrieval. 5 ==> dev; 6 ==> test
          queries = ch_aux.split(",")
          print queries
          for query in queries:
              result = irsys.phrase_query_retrieve(query)
              result = list(result)
              output.append(result)
      elif partId == 7 or partId == 8:
          # TF-IDF. 7 ==> dev; 8 ==> test
          queries = ch_aux.split("; ")
          for query in queries:
              word, docID = query.split(", ")
              result = irsys.get_tfidf_unstemmed(word, int(docID));
              #print 'word: "%s" docID: "%s" result: %f
              output.append(result)
      elif partId == 9 or partId == 10:
          # Cosine Similarity. 9 ==> dev; 10 ==> test
          queries = ch_aux.split(", ")
          for query in queries:
              results = irsys.query_rank(query)
              first_result = [results[0][0], results[0][1]]
              output.append(first_result)
      else:
          print "Unknown partId: %d" % partId
          return None

      if partId in [2,4,6,8,10]:   # test parts
          sys.stdout = out

      # put in the part ID as well (hacky)
      output = str(output)
      #print 'output: %s' % output
      return output

submitter = IRSubmitter()
submitter.submit(0)
