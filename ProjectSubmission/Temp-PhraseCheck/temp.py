file = open('./data/american_english_laga_unna_brown_corpus.txt').read().split()
for word in file:
	if((len(word) != 1) or (word == 'a') or (word == 'I') or (word == 'i') or (word == 'A')):
		print(word.lower()) 