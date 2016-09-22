import pickle
import time
import nltk

import bin.trie

dataPath = './data/'
start = time.time()
pkl_file = open(dataPath + 'context_words.pickle', 'rb')
context_words_dictionary = pickle.load(pkl_file)
intermediate = time.time()

pkl_file_1 = open(dataPath + 'term_frequency.p', 'rb')
term_frequency = pickle.load(pkl_file_1)
end = time.time()

pkl_file_1 = open(dataPath + 'special_confusion_words.p', 'rb')
confusion_sets = pickle.load(pkl_file_1)

coll_dict = {}
coll_dict = open(dataPath + 'collocate_words_1.txt', 'rb').read()

print (intermediate-start)
print (end-intermediate)
# Here, "their" is the target word from the sentence. Replace it with a variable target word in a loop which iterates over each token generated from the sentence

def probability_context_word(target, tokens, INDEX):
	# tokens[INDEX]=target, where tokens is the array obtained from the output of tokenization algorithm.
	confusion_word_set = confusion_sets[target]
	for i in range(0,len(confusion_word_set)):
		confusion_word_set[i] = confusion_word_set[i].strip()

	# Here, we have to append the candidates from spell checker algorithm to confusion_word_set before proceeding

	confusion_word_set.append(target)

	# For every neigbour arrangement, find tags from nltk
	# For every tag arragment, search collocations dictionary
	# Average over each confusion word, if average is zero, give it some delta value
	# Multiply with the probability of context words
	# Choose max
	context_words = {}
	# Iterate over each word in confusion and take different neighbour arrangements
	for word in confusion_word_set:
		temp = context_words_dictionary.get(word)
		for key,value in temp.iteritems():	
			if key in context_words:
				context_words[key] += value
			else:
				context_words[key] = value
		# str1=nltk.os_tag(tokens[INDEX-2]+' '+tokens[INDEX-1]+' 'tokens[INDEX])
		# str2=nltk.os_tag(tokens[INDEX-1]+' '+tokens[INDEX]+' 'tokens[INDEX+1])
		# str3=nltk.os_tag(tokens[INDEX]+' '+tokens[INDEX+1]+' 'tokens[INDEX+2])

	THRESHOLD = 10

	sum_term_frequencies = 0
	for word in confusion_word_set:
		sum_term_frequencies += term_frequency[word]

	relevant_words = []
	for key, value in context_words.iteritems():
		if not ((value < THRESHOLD) or (sum_term_frequencies-value < THRESHOLD)):
			relevant_words.append(key)
	# Compare the context words from the sentence with the relevant_words and then take
	# tokens are the tokenized words for the sentence
	probability = {}
	for candidate in confusion_word_set:
		temp_probability = 1
		for i in range(INDEX-3, INDEX+3):
			if (0 <= i < len(tokens)):
				if(tokens[i] in relevant_words):
					x = context_words_dictionary[candidate][tokens[i]]
					if(x == 0):
						x = 0.001
					temp_probability *= x
		
		temp_probability *= term_frequency[candidate]
		pos = []
		for i in [-1,0,1]:
			if((0 <= INDEX+i-1 < len(tokens)) and (0 <= INDEX+i+1 < len(tokens))):
				z=nltk.os_tag(tokens[INDEX+i-1]+' '+tokens[INDEX+i]+' '+tokens[INDEX+i+1])
				pos.append(z[0][1]+z[1][1]+z[2][1])
		post_score = 0
		for i in len(pos):
			post_score += (1.0*coll_dict[target][pos[i]])/len(pos)
		if(post_score == 0):
			post_score = 0.01
			# To be changed					
		temp_probability *= post_score
		probability[candidate] = temp_probability
	return probability


