from __future__ import division
import os, codecs
from tokenizer import tokenize

DATA_DIR = './data'

# words is a dictionary of all our words
# each key corresponds to a word
# each value is a list of tuples all in the form (sense, definition)
words = dict()

# contexts is the data we're working on
# each element is a triple of the form (word, sense, context)
contexts = []

def read_data():
	global words, contexts

	for filename in os.listdir(DATA_DIR):
		if filename.endswith('.definition'): # test file
			with codecs.open(os.path.join(DATA_DIR, filename), encoding='utf-8') as document:
				definition, word, sense = '', filename.split('.')[0], ''
				words[word] = []
				for line in document:
					if line.startswith('#DEFINITION'): # beginning of a new definition
						sense = line.split()[1].split('%')[1]
					else:
						if line.strip(): # going through definition for last sense
							definition += line
						else: # end of definition for last sense
							words[word].append([sense, definition.strip()])
							definition = ''
				if definition: # definition for last sense
					words[word].append([sense, definition.strip()])
		elif filename.endswith('.test'): # test file
			with codecs.open(os.path.join(DATA_DIR, filename), encoding='utf-8') as document:
				context = ''
				for line in document:
					if line.startswith('#LABEL'):
						word, sense = line.split()[1].split('%')
					else:
						if line.strip(): # going through context for last word-sense pair
							context += line
						else: # end of last context
							contexts.append([word, sense, context.strip()])
							context = ''
				if context: # context for last word-sense pair
					contexts.append([word, sense, context.strip()])
		else: # readme or some other file
			continue

def normalize_data():
	global contexts
	for word in words:
		# converting each sense-definition pair to sense-normalized_definition_tokens
		words[word] = map(lambda pair: [pair[0], tokenize(pair[1])], words[word])
	contexts = map(lambda triple: [triple[0], triple[1], tokenize(triple[2])], contexts)


def overlap(a, b):
	# converting lists to sets
	a, b = set(a), set(b)
	return 2 * len(a & b) / (len(a) + len(b))

def wsd(context, senses):
	'''
	context is the context in which we want to do word sense disambiguation
	senses is a list of sense-definition pairs
	returns the sense with the largest overlap
	'''
	senses = map(lambda pair: [pair[0], overlap(pair[1], context)], senses)
	return sorted(senses, key = lambda pair: pair[1], reverse = True)[0][0]


def main():
	print 'Reading data...'
	read_data()
	print 'Normalizing data...'
	normalize_data()
	print 'Processing...'

	# for each word, 1st element corresponds to the number of correct guesses
	# 2nd element is the number of incorrect guesses
	results = dict(zip(words.keys(), [[0, 0] for i in xrange(len(words))]))
	for ctxt in contexts:
		word, sense, context = ctxt
		result = wsd(context, words[word])
		correct = sense == result
		results[word][0 if correct else 1] += 1
	for k, v in results.items():
		print k, v, v[0]/(sum(v)) * 100
	print 'Total: ', sum([v[0]/(sum(v)) * 100 for v in results.values()])/len(results), len(results)
	print sum(sum(v) for v in results.values()), 'Contexts'

	# # print 'Printing some results...'
	# # Uncomment to print word data
	# for word, senses in words.items():
	# 	print '#' * 45
	# 	print word, len(senses)
	# 	for sense, definition in senses:
	# 		print sense + ': ' + str(definition)
	# 		print
	
	# # Uncomment to print some word-sense-context triples
	# print 	
	# for i in xrange(10):
	# 	print '#' * 45
	# 	print contexts[i]

main()