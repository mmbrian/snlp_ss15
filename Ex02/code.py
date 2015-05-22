from __future__ import division
import os, sys, codecs
from pylab import plt

from math import log10

# log in base 2
lg = lambda x: log10(x)/log10(2)

class Toolkit:
	initialized = False
	__ret = None
	__Nnspam, __Nspam = None, None


	def __init__(self):
		if not Toolkit.initialized:
			Toolkit.init()

	@staticmethod
	def computeInfGain(word):
		'''
		Computes information gain of word in our training set.
				 m
		G(t) = -Sum(P(C_i) x log(P(C_i))) 
				 1
				 	 m
			+ P(t) x Sum(P(C_i|t) x log(P(C_i|t)))
					 1
				_	  m   	   _ 	   	      _	
			+ P(t) x Sum(P(C_i|t) x log(P(C_i|t)))
					  1

		In our problem, we have to classes, namely spam and non-spam
		and P(t) determines how frequent a word has been used
		'''
		if not Toolkit.initialized:
			Toolkit.init()

		# Total number of documents
		T_spam = Toolkit.__Nspam
		T_nspam = Toolkit.__Nnspam
		T = T_spam + T_nspam
		P_spam = T_spam / T

		P_t = sum(Toolkit.__ret[word]) / T
		# for each element in __ret, value is a two-item list, first item is document 
		# frequency in spam training set, second item is document frequncy in non-spam set
		
		P_spam_given_t = Toolkit.__ret[word][0] / sum(Toolkit.__ret[word])
		P_nspam_given_t = Toolkit.__ret[word][1] / sum(Toolkit.__ret[word]) 

		# Here we add +sys.float_info.epsilon for each log term in case conditional probability of 
		# a Class given term is zero.
		return -sum(C_i * lg(C_i) for C_i in (P_spam, 1-P_spam)) + \
				P_t * sum(pcit * lg(pcit + sys.float_info.epsilon) for pcit in (P_spam_given_t, P_nspam_given_t)) + \
				(1-P_t) * sum(pcitb * lg(pcitb + sys.float_info.epsilon) for pcitb in (1-P_spam_given_t, 1-P_nspam_given_t))



	@staticmethod
	def computeMutInf(word):
		'''
		Computes mutual information of word in our training set.

		We use only the spam class here to discriminate well for this category

		I(t,c) = log(P(t, c) / (P(t)P(c)))
			   = log(P(C|t)/P(c))
		'''
		if not Toolkit.initialized:
			Toolkit.init()

		T_spam = Toolkit.__Nspam
		T_nspam = Toolkit.__Nnspam
		T = T_spam + T_nspam

		P_spam = T_spam / T
		P_spam_given_t = Toolkit.__ret[word][0] / sum(Toolkit.__ret[word])
		return lg((P_spam_given_t / P_spam) + sys.float_info.epsilon)

	def get_ret(self):
		# I know, i know, this is dirty but that's what's python's OOP is about! :D
		return Toolkit.__ret
	def get_pspam(self):
		return Toolkit.__Nspam / (Toolkit.__Nspam + Toolkit.__Nnspam)

	@staticmethod
	def init():
		'''
		For each word in the training set, we compute document frequencies in 
		spam and non-spam sets individually and store the result in a dictionary
		(This function makes use of some of the code from wordCounting.py)
		'''
		#insert the paths of the training spam and non spam dataset. Don't remove the r before ''
		pathSpamTrain=r'./dataset/spam-train/'
		pathNonSpamTrain=r'./dataset/nonspam-train/'

		print 'Initializing...'

		ret = dict()
		for filename in os.listdir(pathSpamTrain):
		    with codecs.open(os.path.join(pathSpamTrain, filename), encoding='utf-8') as document:
		        # reading the whole file wouldn't hurt us in this case since they're 
		        # quite short documents
		        content = ''.join(document.readlines()).lower().split()
		        for token in set(content):
		        	if token in ret:
		        		ret[token] += 1
		        	else:	
		        		ret[token] = 1

		# changing value of each token from spam_freq to [spam_freq 0]
		# we are now going to compute the frequency of each token in
		# non spam documents. initially for seen tokens this freq is set to 0
		ret = dict((e, [ret[e], 0]) for e in ret)  
		        
		for filename in os.listdir(pathNonSpamTrain):
		    with codecs.open(os.path.join(pathNonSpamTrain, filename), encoding='utf-8') as document:
				# reading the whole file wouldn't hurt us in this case since they're 
		        # quite short documents
		        content = ''.join(document.readlines()).lower().split()
		        for token in set(content):
		        	if token in ret:
		        		# adding to the freqency in non spam documents
		        		ret[token][1] += 1
		        	else:	
		        		# since this token has not been added to ret before, its document 
		        		# frequency in spam documents is set to zero
		        		ret[token] = [0, 1]

		Toolkit.initialized = True
		print 'Initialization finished...'

		# Number of spam documents
		Toolkit.__Nspam = len(os.listdir(pathSpamTrain))
		# Number of non-spam documents
		Toolkit.__Nnspam = len(os.listdir(pathNonSpamTrain))
		Toolkit.__ret = ret


def main():
	tk = Toolkit()
	# for token in tk.get_ret():
	# 	print token, tk.get_ret()[token]

	print 'Computing document frequencies...'
	print len(tk.get_ret()), 'tokens processed...'
	# for k, v in tk.get_ret().items():
	# 	print k, v
	# 	print 'IG:', tk.computeInfGain(k), 'MI:', tk.computeMutInf(k)
	# print 'P(spam) =', tk.get_pspam()
	tokens = yk.get_ret().items()
	stokens = sorted(tokens, key = lambda x: (x[1][0], x[1][1]))

	wlist = [token[0] for token in tokens]
	IG = [tk.computeInfGain(t) for t in wlist]
	MI = [tk.computeMutInf(t) for t in wlist]
	
	# wlist = ['free', 'mail', 'list', 'com', 'receive', 'send', 'day', 'remove', 'here', 'profit']
	# IG = [tk.computeInfGain(t) for t in wlist]
	# MI = [tk.computeMutInf(t) for t in wlist]

	plt.subplot(111)
	plt.plot(range(len(wlist)), IG, marker='o', color='red', label='IG')
	plt.plot(range(len(wlist)), MI, marker='o', color='blue', label='MI (Spam)')
	plt.xlabel('Word')

	# You can specify a rotation for the tick labels in degrees or with keywords.
	plt.xticks(range(len(wlist)), wlist, rotation='vertical')
	# Pad margins so that markers don't get clipped by the axes
	plt.margins(0.2)
	# Tweak spacing to prevent clipping of tick-labels
	plt.subplots_adjust(bottom=0.15)
	plt.legend()
	plt.show()


main()