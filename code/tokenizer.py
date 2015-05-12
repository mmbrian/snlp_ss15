from __future__ import print_function
from pylab import *
import matplotlib.pyplot  as pyplot

SPLITTING_CHAR_SET = (' ', ',', ".", '!', '?')
NON_TOKEN_CHARS = (' ')

def main():
	print("reading files...")
	f = open('./data/tom_sawyer_en.txt', 'r')
	
	token_list_en = []
	for line in f:
		# enforcing lower case representation
		token_list_en.extend(tokenize(line.lower()))

	print("%d English tokens in general..." % len(token_list_en))
	print("computing frequencies...")
	freq_en = get_frequency_list(token_list_en)
	print("%d unique English tokens..." % len(freq_en))
	f.close()

	f = open('./data/tom_sawyer_de.txt', 'r')
	token_list_de = []
	for line in f:
		# enforcing lower case representation
		token_list_de.extend(tokenize(line.lower()))
	
	print("%d Deutsch tokens in general..." % len(token_list_de))
	print("computing frequencies...")
	freq_de = get_frequency_list(token_list_de)
	print("%d unique Deutsch tokens..." % len(freq_de))
	f.close()

	f = open('./data/tom_sawyer_fin.txt', 'r')
	token_list_fin = []
	for line in f:
		# enforcing lower case representation
		token_list_fin.extend(tokenize(line.lower()))
	
	print("%d Finish tokens in general..." % len(token_list_fin))
	print("computing frequencies...")
	freq_fin = get_frequency_list(token_list_fin)
	print("%d unique Finish tokens..." % len(freq_fin))
	f.close()

	print("displaying zipf plot...")
	plot_zipf(freq_en, freq_de, freq_fin)


def tokenize(s):
	tokens, token = [], ''
	for c in s:
		if c in SPLITTING_CHAR_SET:
			tokens.append(token)
			if c not in NON_TOKEN_CHARS:
				tokens.append(c) # adding special characters as separate tokens
			token = ''
		else:
			token += c
	return tokens

def get_frequency_list(tokens):
	keys = list(set(tokens))
	values = [tokens.count(k) for k in keys]
	# returning tokens sorted according to their frequency
	return sorted(zip(keys, values), key=lambda e:e[1], reverse = True) # reversing for desc order

def plot_zipf(*freq):
	ranks, frequencies = [], []
	langs = ("English", "German", "Finish")
	colors = ('red', 'green', 'blue')


	with plt.xkcd():
		plt.subplot(111) # 1, 1, 1

		for i in xrange(3):
			ranks.append(range(1, len(freq[i]) + 1))
			frequencies.append([e[1] for e in freq[i]])

			# log x and y axis	
			plt.loglog(ranks[i], frequencies[i], basex=2, color=colors[i], label=langs[i])

		plt.legend()
		plt.grid(True)
		plt.title("Zipf's law!")

		plt.xlabel('Rank')
		plt.ylabel('Frequency')

	plt.show()

main()
