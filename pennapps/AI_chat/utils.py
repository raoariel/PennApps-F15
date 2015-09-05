# Get text
# go with most recent
# traits:
#   - caps usage
#   - grammar nazi
#     - perfect grammar SKIP
#     - formality :: capital i, contractions, etc. 
#   - use of ...
#   - smilies and which
#   - block messaging
#   - exclamation marks
#   - 'slang'

import os, sys, re, string, ast, json

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
    self.used_slang = set()
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
    # slang which can be interchangeable used, for the most part
    self.slang = {'omg','lol','mkay','atm','rotfl'}
    self.word_count = 0
    for m in messages:
      m_words = m['message'].split()
      self.setTraitCaps(m_words)
      self.setTraitFormality(m_words)
      self.setTraitEllipsesExclamation(m_words)
      self.setTraitEmoticon(m_words)
      self.setTraitBlocking(m_words)
      self.setTraitSlang(m_words)
      self.setTraitFiller(m_words)
    self.blocking = (self.word_count / self.message_count) > 8
    return 
  
  def setTraitSlang(self, message):
    # for each message, split space, 
    # check is caps , or .. in list etc.
    for slang in self.slang:
      if slang in message:
        self.used_slang.add(slang)
    return 

  def setTraitCaps(self, message):
    # cap leters over totall leters by avg letter 
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
    traits['used_slang'] = self.used_slang # set
    return traits
