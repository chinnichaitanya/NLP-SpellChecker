import pickle
import time
import bin.trie

dataPath = './data/'
start = time.time()
pkl_file= open(dataPath + 'context_words.pickle', 'rb')
context_words_dictionary = pickle.load(pkl_file)
intermediate = time.time()
pkl_file_1 = open(dataPath + 'term_frequency.p', 'rb')
term_frequency = pickle.load(pkl_file_1)
end = time.time()
pkl_file_1 = open(dataPath + 'special_confusion_words.p', 'rb')
confusion_sets = pickle.load(pkl_file_1)

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

	context_words = {}
	for word in confusion_word_set:
		temp = context_words_dictionary.get(word)
		# print temp
		for key,value in temp.iteritems():	
			if key in context_words:
				context_words[key] += value
			else:
				context_words[key] = value

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
		temp_probability = 0
		for i in range(INDEX-3, INDEX+3):
			if (0 <= i < len(tokens)):
				if(tokens[i] in relevant_words):
					if(temp_probability == 0):
						temp_probability = 1.0*context_words_dictionary[candidate][tokens[i]]/term_frequency[candidate]
					else:
						temp_probability *= 1.0*context_words_dictionary[candidate][tokens[i]]/term_frequency[candidate]
		temp_probability *= term_frequency[candidate]
		probability[candidate] = temp_probability
	return probability


