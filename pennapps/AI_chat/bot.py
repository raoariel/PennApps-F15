import nltk
import string
import os
import json
import indicoio
import operator
import urllib2
import cleverbot
from random import randint
from utils import GetData, ParseTraits

from chatterbotapi import ChatterBotFactory, ChatterBotType

indicoio.config.api_key = 'cd64ad1143b5abb73cae12457098e7aa'

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
from nltk.collocations import *

bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

token_dict = {}
stops = set(stopwords.words('english'))
fillers = ['hmmm..', 'uhh..', 'umm..', 'yeah..']

gif_counter = 0
ellipses = 0


# Chatting traits:
# - use of filler words
# - using common phrases
# - all small letters
# - no '
# - capital
# - smileys
# - ...

# cb = cleverbot.Cleverbot()

def tokenize(text):
	tokens = nltk.word_tokenize(text)
	stems = []
	for item in tokens:
	    stems.append(PorterStemmer().stem(item))
	return stems

def get_messages_from_json():
	with open('output') as data_file:    
		data = json.load(data_file)
    	for item in data["data"]:
    		msgs = ""
    		for msg in item["comments"]['data']:
    			if 'message' in msg.keys():
    				# print item['id'] + " --- " + msg['message']
    				s = "\n" + msg['message'].lower()
    				msgs += s
    		x = item['id']
    		token_dict[x] = msgs

# get_messages_from_json()

# for k,v in token_dict.iteritems():
# 	print k + " : " + v

# tfidf = TfidfVectorizer(tokenizer=tokenize, stop_words='english')
# tfs = tfidf.fit_transform(token_dict.values())

# query = 'bye'
# response = tfidf.transform([query])
# print response

# feature_names = tfidf.get_feature_names()
# for col in response.nonzero()[1]:
#     print feature_names[col], ' - ', response[0, col]


# Manual Search for bag of words
sentences = []
word_count = {}
for thread in token_dict.values():
	msgs = thread.split('\n')
	for i in range(len(msgs)):
		# Check if query word is in sentence
		for each_word in query.split():
			if each_word.lower() in msgs[i].split():
				print msgs[i]
				print "Response : " + msgs[i+1]
				print "\n\n"
				sentences.append(msgs[i])

		# Get frequently used words
		for each_word in msgs[i].split():
			each_word = each_word.lower()
			if each_word not in stops:
				if each_word in word_count.keys():
					word_count[each_word] += 1
				if each_word not in word_count.keys():
					word_count[each_word] = 1

sorted_word_count_dict = sorted(word_count.items(), key=operator.itemgetter(1), reverse=True)

# for x in sorted_word_count_dict:
# 	print x

# Extract bi-gram/tri-gram 
all_msgs_str = ""
for each_thread in token_dict.values():
	each_thread += " "
	all_msgs_str += each_thread

# Bigram
# tokens = nltk.wordpunct_tokenize(all_msgs_str)
tokens = all_msgs_str.split()
finder = BigramCollocationFinder.from_words(tokens)
finder.apply_freq_filter(3) 
# print finder.nbest(bigram_measures.pmi, 10)  

#Trigram
finder = TrigramCollocationFinder.from_words(tokens)
finder.apply_freq_filter(3) 
# print finder.nbest(trigram_measures.pmi, 10)  



# Apply sentiment analysis on these sentences
# for sentence in sentences:
# 	print str(indicoio.sentiment(sentence)) + " -- " + sentence


# Giphy API url
def get_gif(query):
	giphy_query = query.replace(' ', '+')
	# giphy_query = "eating+cereal"
	giphy_url = 'http://api.giphy.com/v1/gifs/search?q=' + giphy_query
	giphy_key = 'dc6zaTOxFJmzC'
	giphy_url += '&api_key='
	giphy_url += giphy_key
	data = json.load(urllib2.urlopen(giphy_url))
	return data['data'][0]['embed_url']
# print data['data'][0]['embed_url']

def get_traits():
	get_data = GetData()
	data = get_data.getDataValues()
	trait_parser = ParseTraits(data)
	return trait_parser.getTraits()

factory = ChatterBotFactory()

bot1 = factory.create(ChatterBotType.CLEVERBOT)
bot1session = bot1.create_session()

bot2 = factory.create(ChatterBotType.PANDORABOTS, 'b0dafd24ee35a477')
bot2session = bot2.create_session()

traits = get_traits()
print traits



def get_bot_response(user_message):
	global gif_counter, ellipses
	if 'name?' in user_message:
		return "i'm animesh.."
	if 'who are you?' in user_message:
		return "you know me.."

	if 'where' in user_message and 'live?' in user_message:
		return "in Bangalore, India"
	# Checking for GIF usage
	if 'ing' in user_message:
		gif_counter += 1
		if gif_counter % 2 == 0:
			user_message = user_message.lower()
			user_message = ' '.join([word for word in user_message.split() if word not in stops])
			user_message.strip()
			gif_url = get_gif(s)
			return gif_url

	resp = bot1session.think(user_message).lower()
	if '?' in user_message:
		resp = fillers[randint(0,len(fillers)-1)] + " " + resp
	sentiment = indicoio.sentiment(resp)
	resp.replace("'", '')
	# print sentiment

	if traits['ellipses_count'] > 10:
		ellipses += 1
		if ellipses % 5 == 0:
			resp += "... "

	if sentiment > 0.90:
		resp += "!!!"
	if sentiment > 0.8:
		resp += " :)"
	if sentiment < 0.15:
		resp += " :("

	return resp



while (1):
	s = raw_input("you : ")
	resp = get_bot_response(s)
	print "shadow : " + resp






