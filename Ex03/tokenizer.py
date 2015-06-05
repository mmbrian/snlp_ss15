from __future__ import print_function
import codecs
from pylab import plt
import nltk
from nltk.stem.lancaster import LancasterStemmer
import sys

# TODO: in the end, experiment with snowball stemmer and compare results!
en_stem = nltk.snowball.EnglishStemmer().stem
# en_stem = LancasterStemmer().stem

# We're just using this stop word list from nltk, we could as well copy paste the list here
stop_words = nltk.corpus.stopwords.words('english')

# punctuation marks
SPLITTING_CHAR_SET = (' ', ',', ".", "'", '!', '?', ';', ':', '"', ')', '(', '[', ']', '{', '}')

bonus_part = False

def tokenize(s, stem = True):
	'''
	s is a string to tokenize
	stem enabled would apply stemming
	'''
	tokens, token = [], ''
	for c in s.lower():
		if c in SPLITTING_CHAR_SET:
			if token and not token in stop_words:
				if stem: token = en_stem(token)
				tokens.append(token)
			token = ''
		else:
			token += c
	return tokens
