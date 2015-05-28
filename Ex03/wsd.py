from __future__ import division
import os, codecs

DATA_DIR = './data'

words = dict()
contexts = []

def process_data():
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
							words[word].append((sense, definition.strip()))
							definition = ''
				if definition: # definition for last sense
					words[word].append((sense, definition.strip()))
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
							contexts.append((word, sense, context.strip()))
							context = ''
				if context: # context for last word-sense pair
					contexts.append((word, sense, context.strip()))
		else: # readme or some other file
			continue

def main():
	print 'Processing data...'
	process_data()

	print 'Printing some results...'
	
	## Uncomment to print word data
	# for word, senses in words.items():
	# 	print '#' * 45
	# 	print word, len(senses)
	# 	for sense, definition in senses:
	# 		print sense + ': ' + definition
	# 		print
	
	## Uncomment to print some word-sense-context triples
	# print 	
	# for i in xrange(10):
	# 	print '#' * 45
	# 	print contexts[i]

main()