# Web scraping
import urllib
from bs4 import BeautifulSoup

# Text summarization
import re
import random
from summarize import *

# Image Manipulation
import PIL
from PIL import ImageFont
from PIL import Image
from PIL import ImageDraw
from random import randint,shuffle

class DogeMachine(object):
	def __init__(self,article="http://www.theonion.com/article/gay-teen-worried-he-might-be-christian-2888", dogeLoc='doge.jpeg'):
		self.article = article
		self.doge = dogeLoc
		self.getContent()
		self.summarizeContent()

	def getContent(self):
		# Scrape the site for the article content
		html = urllib.urlopen(self.article).read()
		soup = BeautifulSoup(html)
		[s.extract() for s in soup(['style', 'script', '[document]', 'head', 'title'])]
		self.visible_text = soup.getText()
		return

	def summarizeContent(self):
		# Summarize article and get main words
		ss = SimpleSummarizer()
		input = self.visible_text
		summaryLen = 1
		summary = ss.summarize(input,summaryLen)
		words = summary.split()
		filteredWords = [word for word in words if (word not in stopwords.words('english') and (not bool(re.search(r'\d', word))))]
		filteredWords = set(filteredWords)
		self.dogeWords = random.sample(filteredWords, min(len(filteredWords),5))
		return

	def getDogeWords(self):
		return self.dogeWords