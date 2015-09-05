# Get text
# go with most recent
# traits:
#   - caps usage
#   - grammar nazi
#     - perfect grammar
#     - formality :: capital i, contractions, etc. 
#   - use of ...
#   - smilies and which
#   - block messaging
#   - exclamation marks
#   - 'slang'

import os, sys, re, string, ast, json
from  nltk import *
from corenlp import *
from pprint import pprint

class GetData(object):
  def __init__(self,dataDir='../sampleMessages.json'):
    """Extract relevant data from Facebook inbox message object"""
    with open(dataDir) as data_file:    
        self.data = json.load(data_file)
    self.setDataValues()
    return

  def setDataValues(self):
    self.conversation_data = self.data['inbox']['data']
    self.message_data = []
    for c in self.conversation_data:
      try:
        conversation = c['comments']['data']
        for m in conversation:
          curr_message = {}
          curr_message['from'] = m['from']['name']
          try:
            curr_message['message'] = m['message']
            self.message_data.append(curr_message)
          except:
            pass # no messages stored here
      except: 
        pass # no messages stored here
    return 

  def getDataValues(self):
    return self.message_data
  

class ParseTraits(object):
  def __init__(self,messages):
    """Quick pass over own messages to get user messaging traits"""
    self.me = 'Ariel Rao' # need to get dynamically
    self.message_count = len(messages)
    self.caps = set()
    self.ellipses_count = 0
    self.exclamation_count = 0
    self.formality_I = True
    self.used_contractions = {}
    self.filler = set()
    self.emoticons = {
      ":)": 0,
      ":D": 0,
      ":(": 0,
      ":'(": 0,
      ":P": 0,
      "O:)": 0,
      "3:)": 0,
      "o.O": 0,
      ";)": 0,
      ':P': 0,
      ':)': 0,
      ':P': 0,
      ':)': 0
    }
    self.contractions = {
      'dont': "don't", 
      'wont': "won't", 
      'cant': "can't", 
      'ive': "I've", 
      'youre': "you're", 
      'didnt': "didn't", 
      'shes': "she's", 
      'theyre': "they're", 
      'youve': "you've", 
      'arent': "aren't", 
      'lets': "let's", 
      'weve': "we've"
    } 
    self.word_count = 0
    for m in messages:
      m_words = m['message'].split()
      self.setTraitCaps(m_words)
      self.setTraitFormality(m_words)
      self.setTraitEllipsesExclamation(m_words)
      self.setTraitEmoticon(m_words)
      self.setTraitBlocking(m_words)
      # self.setTraitGrammar(m_words)
      # self.setTraitSlang(m_words)
      self.setTraitFiller(m_words)
    self.blocking = (self.word_count / self.message_count) > 8
    return 
  
  def setTraitSlang(self, message):
    # for each message, split space, 
    # check is caps , or .. in list etc.
    return 

  def setTraitCaps(self, message):
    # cap leters over totall leters by avg letter 
    # maybe just regex for LOL and HAHAs
    #usage:: when generating message, see if words in message in this set, then change accordingly
    for word in message:
      if (word.isupper() and (word not in self.emoticons)):
        self.caps.add(word)
    return 

  def setTraitFormality(self, message):
    # capial i, apostrophes'
    for word in message:
      if 'i' == word:
        self.formality_I = False
      elif word in self.contractions:
        # hard eg. we're vs were 
        self.used_contractions[self.contractions[word]] = word
    return 
  
  def setTraitEllipsesExclamation(self, message):
    for word in message:
      if '...' in word:
        # at least 3 to count
        self.ellipses_count += 1
      if '!' in word:
        # at least 1 to count
        self.ellipses_count += 1
    return 
  
  def setTraitEmoticon(self, message):
    for word in message:
      if word in self.emoticons:
        self.emoticons[word] += 1    
    return 
  
  def setTraitBlocking(self, message):
    self.word_count += len(message)
    return 
  
  # def setTrait_grammar(self, message):
  #   """not mvp"""
  #   return 
  
  # def setTrait_slang(self, message):
  #   """not mvp"""
  #   return 
  
  def setTraitFiller(self, message):
    """not mvp, but like umm, hmm, well.. mhm mm uhhh ehh"""
    regs = {r'^um+$', r'^hm+$', r'^well+$', r'^mhm+$', r'^mm+$', r'^uh+$', r'^eh+$'}
    for word in message:
      for reg in regs:
        filler = re.search(reg, word)
        if filler:
          self.filler.add(filler.group())
    return 

  def getTraits(self):
    traits = {}
    traits['filler'] = self.filler # set
    traits['emoticons'] = self.emoticons # dict count
    traits['formality_I'] = self.formality_I # bool
    traits['used_contractions'] = self.used_contractions # dict map
    traits['caps'] = self.caps # set
    traits['ellipses_count'] = self.ellipses_count # int
    traits['exclamation_count'] = self.exclamation_count # int
    traits['blocking'] = self.blocking # bool
    return traits

class GetTopics(object):
  def __init__(self,messages):
    """Get NER to use for topic selection"""
    self.messages = messages
    self.ner = set()
    self.parses = set()
    self.corenlp = StanfordCoreNLP()
    self.setNER()

  def setNER(self,maxParse=20):
    i = 1
    for message in self.messages:
      text = message['message']
      if isinstance(text, unicode):
        text = text.encode('ascii', 'xmlcharrefreplace')
      try:
        parse = json.loads(self.corenlp.parse(text))
        self.parses.add(parse)
        sentences = parse['sentences']
        for sentence in sentences:
          words = sentence['words']
          for word in words:
            wordData = word[1]
            if wordData['NamedEntityTag'] != 'O':
              if not bool(re.search(r'\d', word[0])):
                self.ner.add(word[0])
      except:
        print 'Parse failed %s' % text
      i += 1
      if i > maxParse: break

  def getNER(self):
    return self.ner



