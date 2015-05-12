from __future__ import print_function

SPLITTING_CHAR_SET = (' ', ',', ".", '!', '?')

def main():
	f = open('./data/tom_sawyer_en.txt', 'r')
	token_list = []
	for line in f:
		token_list.extend(tokenize(line.lower()))
	print(len(token_list))
	for i in xrange(100):
		print(token_list[i])


def tokenize(s):
	tokens, token = [], ''
	for c in s:
		if c in SPLITTING_CHAR_SET:
			tokens.append(token)
			if c is not ' ':
				tokens.append(c) # adding special characters as separate tokesn
			token = ''
		else:
			token += c
	return tokens

main()
