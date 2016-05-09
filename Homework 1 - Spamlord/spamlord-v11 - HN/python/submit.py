import urllib
import urllib2
import hashlib
import random
import email
import email.message
import email.encoders
import StringIO
import sys

from shared_submit import Submitter

import SpamLord

class NullDevice:
  def write(self, s):
    pass

def dumps_list_of_lists(res):
  """Deprecated version of JSON encoder. Used as a fallback if python cannot import json library."""
  s = '['
  for i, l in enumerate(res):
    if (i != 0):
      s += ', '
    s += '['
    for j, e in enumerate(l):
      if (j != 0):
        s += ', '
      s += '\"%s\"' % e
    s += ']'
  s += ']'
  return s


class SpamLordSubmitter(Submitter):
  def validParts(self):
    """Returns a list of valid part names."""
    partNames = ['Development Set', \
                  'Test Set'
                ]
    return partNames

  def sources(self):
    """Returns source files, separated by part. Each part has a list of files."""
    srcs = [ [ 'SpamLord.py' ], \
             [ 'SpamLord.py' ],
           ]
    return srcs

  def homework_id(self):
    """Returns the string homework id."""
    return '1'

  def output(self, partId, ch_aux):
    """Uses the student code to compute the output for test cases."""

    res = []
    print '== Running your code ...'
    # disable printing:
    original_stdout = sys.stdout
    sys.stdout = NullDevice()
    if(partId==1):
      train_data = ''
      res = SpamLord.process_dir('../data/dev')
    elif(partId==2):
      test_data = StringIO.StringIO(ch_aux)
      res = SpamLord.process_file('foo', test_data)
    else:
      sys.stdout = original_stdout
      print '[WARNING]\t[output]\tunknown partId: %s' % partId
    sys.stdout = original_stdout
    print '== Finished running your code'
    try:
      import json
      res_json = json.dumps(res)
    except ImportError:
      print '!!! Error importing json library. This is likely due to an early version of Python 2.6. Attempting to submit without json library. If this fails, please update to Python 2.7.'
      res_json = dumps_list_of_lists(res)
    return res_json

submitter = SpamLordSubmitter()
submitter.submit(0)
