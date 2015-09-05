# Get text
# go with most recent
# traits:
#   - caps usage
#   - grammar nazi
#     - perfect grammar
#     - formality :: capital i, apostrophes, etc. 
#   - use of ...
#   - smilies and which
#   - block messaging
#   - exclamation marks
#   - 'slang'

import json
from pprint import pprint

class GetData(object):
  def __init__(self,dataDir='sampleMessages.json'):  
    with open(dataDir) as data_file:    
        self.data = json.load(data_file)
    self.setDataValues()
    return

  def setDataValues(self):
    self.conversation_data = self.data['inbox']['data']
    self.message_data = []
    for c in self.conversation_data:
      conversation = c['comments']['data']
      for m in conversation:
        curr_message = {}
        curr_message['from'] = m['from']['name']
        curr_message['message'] = m['message']
        self.message_data.append(curr_message)
    return 

  def getDataValues(self):
    return self.message_data
  

class ParseTraits(object):
  def __init__(self,messages):
    """."""
    self.me = 'Ariel Rao'
    self.message_count = len(messages)
    self.caps = set()
    self.ellipses_count = 0
    self.exclamation_count = 0
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
    self.word_count = 0
    for m in messages:
      m_words = m['message'].split()
      self.set_trait_caps(m_words)
      # self.set_trait_formality(m_words)
      self.set_trait_ellipses_exclamation(m_words)
      self.set_trait_emoticon(m_words)
      self.set_trait_blocking(m_words)
      # self.set_trait_grammar(m_words)
      # self.set_trait_slang(m_words)
      self.set_trait_filler(m_words)
    self.blocking = (self.word_count / self.message_count) > 8
    return 
  
  def set_trait_slang(self, message):
    # for each message, split space, 
    # check is caps , or .. in list etc.
    return 

  def set_trait_caps(self, message):
    # cap leters over totall leters by avg letter 
    # maybe just regex for LOL and HAHAs
    #usage:: when generating message, see if words in message in this set, then change accordingly
    for word in message:
      if (word.isupper() and (word not in self.emoticons):
        self.caps.add(word)
    return 

  # def set_trait_formality(self, message):
  #   # capial i, apostrophes
  #   return 
  
  def set_trait_ellipses_exclamation(self, message):
    for word in message:
      if '...' in word:
        # at least 3 to count
        self.ellipses_count += 1
      if '!' in word:
        # at least 1 to count
        self.ellipses_count += 1
    return 
  
  def set_trait_emoticon(self, message):
    for word in message:
      if word in self.emoticons:
        self.emoticons[word] += 1    
    return 
  
  def set_trait_blocking(self, message):
    self.word_count += len(message)
    return 
  
  # def set_trait_grammar(self, message):
  #   """not mvp"""
  #   return 
  
  # def set_trait_slang(self, message):
  #   """not mvp"""
  #   return 
  
  def set_trait_filler(self, message):
    """not mvp, but like umm, hmm, well.. mhm mm uhhh ehh"""
    regs = {r'^um+$', r'^hm+$', r'^well+$', r'^mhm+$', r'^mm+$', r'^uh+$', r'^eh+$'}
    for word in message:
      for reg in regs:
        filler = re.search(reg, word)
        if filler:
          self.filler.add(filler)
    return 
  
  




  # trigger words












 a = re.search(reg, 'uhhhj')
>>> reg = r'^uh+$'






















