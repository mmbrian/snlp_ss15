from __future__ import print_function
import codecs
from pylab import plt
import nltk
import sys

en_stem = nltk.snowball.EnglishStemmer().stem
de_stem = nltk.snowball.GermanStemmer().stem
fi_stem = nltk.snowball.FinnishStemmer().stem

# punctuation marks
SPLITTING_CHAR_SET = (' ', ',', ".", "'", '!', '?', ';', ':')
NON_TOKEN_CHARS = (' ')

bonus_part = False

def main():
	global bonus_part
	bonus_part = False
	if len(sys.argv) > 1:
		if sys.argv[1] == "bonus":
			bonus_part = True

	print("reading files...")
	f = codecs.open('./data/tom_sawyer_en.txt', encoding='utf-8')
	token_list_en, stem_list_en = [], []
	for line in f:
		# Normalizing to lowercase before tokenization
		nline = line.lower()
		token_list_en.extend(tokenize(nline))
		if bonus_part:
			stem_list_en.extend(tokenize(nline, True, 'en'))

	freq_en, sfreq_en, freq_de, sfreq_de, freq_fin, sfreq_fin = [], [], [], [], [], []

	print("%d English tokens in general..." % len(token_list_en))
	print("Computing frequencies...")
	freq_en = get_frequency_list(token_list_en)
	print("%d unique English tokens..." % len(freq_en))
	if bonus_part:
		sfreq_en = get_frequency_list(stem_list_en)
		print("%d unique English stems..." % len(sfreq_en))
	f.close()

	f = codecs.open('./data/tom_sawyer_de.txt', encoding='utf-8')
	token_list_de, stem_list_de = [], []
	for line in f:
		# Normalizing to lowercase before tokenization
		nline = line.lower()
		token_list_de.extend(tokenize(nline))
		if bonus_part:
			stem_list_de.extend(tokenize(nline, True, 'de'))
	
	print("%d Deutsch tokens in general..." % len(token_list_de))
	print("Computing frequencies...")
	freq_de = get_frequency_list(token_list_de)
	print("%d unique Deutsch tokens..." % len(freq_de))
	if bonus_part:
		sfreq_de = get_frequency_list(stem_list_de)
		print("%d unique Deutsch stems..." % len(sfreq_de))
	f.close()

	f = codecs.open('./data/tom_sawyer_fin.txt', encoding='utf-8')
	token_list_fin, stem_list_fin = [], []
	for line in f:
		# Normalizing to lowercase before tokenization
		nline = line.lower()
		token_list_fin.extend(tokenize(nline))
		if bonus_part:
			stem_list_fin.extend(tokenize(nline, True, 'fi'))	
	
	print("%d Finnish tokens in general..." % len(token_list_fin))
	print("Computing frequencies...")
	freq_fin = get_frequency_list(token_list_fin)
	print("%d unique Finnish tokens..." % len(freq_fin))
	if bonus_part:
		sfreq_fin = get_frequency_list(stem_list_fin)
		print("%d unique Finnish stems..." % len(sfreq_fin))
	f.close()

	print("displaying zipf plot...")
	plot_zipf(freq_en, freq_de, freq_fin, sfreq_en, sfreq_de, sfreq_fin)


def tokenize(s, stem = False, lang = ''):
	'''
	s is a string to tokenize
	stem enabled would apply stemming
	lang determines the language for stemming
	'''
	tokens, token = [], ''
	for c in s:
		if c in SPLITTING_CHAR_SET:
			if token:
				if bonus_part: # apply stemming
					if lang == 'en':
						token = en_stem(token)
					elif lang == 'de':
						token = de_stem(token)
					elif lang == 'fi': # Finnish
						token = fi_stem(token)
				tokens.append(token)
			# Uncomment the lines below in order to include punctuations in zipf's plot	
			# if c not in NON_TOKEN_CHARS:
				# tokens.append(c) # adding special characters as separate tokens
			token = ''
		else:
			token += c
	return tokens

def get_frequency_list(tokens):
	# removing redundant words by taking set of tokens
	keys = list(set(tokens))
	# counting token frequencies
	values = [tokens.count(k) for k in keys]
	# returning tokens sorted according to their frequency
	return sorted(zip(keys, values), key=lambda e:e[1], reverse = True) # reversing for desc order

def plot_zipf(*freq):
	'''
	basic plotting using matplotlib and pylab
	'''
	ranks, frequencies = [], []
	langs, colors = [], []
	langs = ["English", "German", "Finnish"]
	colors = ['#FF0000', '#00FF00', '#0000FF']
	if bonus_part:
		colors.extend(['#00FFFF', '#FF00FF', '#FFFF00'])
		langs.extend(["English (Stemmed)", "German (Stemmed)", "Finnish (Stemmed)"])

	plt.subplot(111) # 1, 1, 1

	num = 6 if bonus_part else 3
	for i in xrange(num):
		ranks.append(range(1, len(freq[i]) + 1))
		frequencies.append([e[1] for e in freq[i]])

		# log x and y axi, both with base 10
		plt.loglog(ranks[i], frequencies[i], marker='', basex=10, color=colors[i], label=langs[i])

	plt.legend()
	plt.grid(True)
	plt.title("Zipf's law!")

	plt.xlabel('Rank')
	plt.ylabel('Frequency')

	plt.show()

main()
