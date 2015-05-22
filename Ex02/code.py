from __future__ import division
import os, sys, codecs
from pylab import plt
from random import sample

from math import log10

from Classification import classify

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

		T_spam = Toolkit.__Nspam
		T_nspam = Toolkit.__Nnspam
		T = T_spam + T_nspam

		# Estimating necessary probabilities based on our data
		P_spam = T_spam / T
		P_t = sum(Toolkit.__ret[word]) / T # the sum term adds document freq. in spam and non-spam sets

		# for each element in __ret, value is a two-item list, first item is document 
		# frequency in spam training set, second item is document frequncy in non-spam set
		P_spam_given_t = Toolkit.__ret[word][0] / sum(Toolkit.__ret[word])
		P_nspam_given_t = Toolkit.__ret[word][1] / sum(Toolkit.__ret[word]) 

		# Here we add +sys.float_info.epsilon for each log term in case conditional probability of 
		# a Class given term is zero. (first lot term is never 0 here)
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

	classification = False
	if len(sys.argv) > 1:
		if sys.argv[1].lower() == "classification":
			classification = True


	print 'Computing document frequencies...'
	print len(tk.get_ret()), 'tokens processed...'

	# Uncomment this part to get info on all tokens
	# for k, v in tk.get_ret().items():
	# 	print k, v
	# 	print 'IG:', tk.computeInfGain(k), 'MI:', tk.computeMutInf(k)
	# print 'P(spam) =', tk.get_pspam()
	# tokens = tk.get_ret().items()
	## Filtering tokens based on their document frequency
	# tokens = filter(lambda x:sum(x[1]) > 40, tokens)
	## Sorting them first with regard to their document frequency in spam set, then non-spam set
	# stokens = sorted(tokens, key = lambda x: (x[1][0], x[1][1]))

	# Uncomment this part to get 10 random tokens
	# wlist = [token[0] for token in tokens]
	# wlist = sample(wlist, 10)
	# IG = [tk.computeInfGain(t) for t in wlist]
	# MI = [tk.computeMutInf(t) for t in wlist]
	# print wlist


	# wlist = [u'understand', u'remove', u'paul', u'leave', u'response', u'cash', u'hear', u'necessary', u'view', u'p']
	wlist = [u'free', u'mail', u'list', u'com', u'receive', u'send', u'day', u'remove', u'here', u'profit']

	IG = [tk.computeInfGain(t) for t in wlist]
	MI = [tk.computeMutInf(t) for t in wlist]

	if not classification:	
		plt.subplot(111)
		plt.plot(range(len(wlist)), IG, marker='o', color='red', label='IG')

		# plt.ylabel('Information Gain')
		# # You can specify a rotation for the tick labels in degrees or with keywords.
		# plt.xticks(range(len(wlist)), wlist, rotation='horizontal')
		# # Pad margins so that markers don't get clipped by the axes
		# plt.margins(0.2)
		# # Tweak spacing to prevent clipping of tick-labels
		# plt.subplots_adjust(bottom=0.15)
		# plt.legend()

		# plt.subplot(212)
		plt.plot(range(len(wlist)), MI, marker='o', color='blue', label='MI (Spam)')
		# plt.ylabel('Mutual Information')

		plt.xlabel('Word')

		# You can specify a rotation for the tick labels in degrees or with keywords.
		plt.xticks(range(len(wlist)), wlist, rotation='vertical')
		# Pad margins so that markers don't get clipped by the axes
		plt.margins(0.2)
		# Tweak spacing to prevent clipping of tick-labels
		plt.subplots_adjust(bottom=0.15)
		plt.legend(loc=2) # upper left
		plt.show()
	else:

		# here we want to sort our data based on MI and IG, so first we stitch everything
		# together so we can keep track of them after sorting
		tlist = zip(wlist, IG, MI)
		# sorting based on the 3rd element (MI)
		tlist_MI = sorted(tlist, key = lambda x: x[2], reverse = True)[:5] # only top five (desc)
		# sorting based on the 2nd element (IG)
		tlist_IG = sorted(tlist, key = lambda x: x[1], reverse = True)[:5]

		# Here we compute classification results for each of these attribute sets:
		# 1st word with highest MI
		# 1st two words with highest MI
		# ...
		# All top 5 words with highest MI
		MI_cls = [classify(set(e[0] for e in tlist_MI[:i])) for i in range(1, len(tlist_MI)+1)]
		
		plt.subplot(211)
		plt.plot([e[2] for e in tlist_MI], MI_cls, marker='o', color='red', label='MI (Spam)')
		plt.ylabel('Misclassifications')
		plt.legend(loc=2)

		# same as before for IG
		IG_cls = [classify(set(e[0] for e in tlist_IG[:i])) for i in range(1, len(tlist_IG)+1)]

		plt.subplot(212)
		plt.plot([e[1] for e in tlist_IG], IG_cls, marker='o', color='blue', label='IG')
		plt.ylabel('Misclassifications')
		plt.legend(loc=2) # upper left
		
		plt.show()


main()