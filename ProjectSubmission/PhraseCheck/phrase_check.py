import time
import pickle

from bin.trie import *
from bin.editex import *
from bin.bayesian import *
from bin.stringTokenize import *

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
	confusion_word_set = confusion_sets.get(target, [])
	for i in range(0,len(confusion_word_set)):
		confusion_word_set[i] = confusion_word_set[i].strip()

	# Here, we have to append the candidates from spell checker algorithm to confusion_word_set before proceeding
	targetCandidates = trie.getCandidates(target, 2)
	# bayesianProbabilityArray = get_bayesian_probabilities(target, targetCandidates)
	phoneticProbabilityArray = get_phonetic_probabilities(target, targetCandidates)
	totalProbabilityArray = [p for p in phoneticProbabilityArray]
	# totalProbabilityArray = [p*b for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
	totalDict = []
	for i in range(0, len(targetCandidates)):
		totalDict.append((targetCandidates[i], totalProbabilityArray[i]))
	
	totalDict = sorted(totalDict, key=lambda x: x[1], reverse=True)
	words_from_spellcheck = []
	for i in range(0, 11):
		words_from_spellcheck.append(totalDict[i][0])

	confusionSet[target] = words_from_spellcheck

	confusion_word_set.append(target)

	confusion_word_set.extend(words_from_spellcheck)

	context_words = {}
	for word in confusion_word_set:
		temp = context_words_dictionary.get(word, {})
		# print temp
		for key, value in temp.items():	
			if key in context_words:
				context_words[key] += value
			else:
				context_words[key] = value

	THRESHOLD = 10

	sum_term_frequencies = 0
	for word in confusion_word_set:
		sum_term_frequencies += term_frequency.get(word, 0)

	relevant_words = []
	for key, value in context_words.items():
		if not ((value < THRESHOLD) or (sum_term_frequencies-value < THRESHOLD)):
			relevant_words.append(key)
	# Compare the context words from the sentence with the relevant_words and then take
	# tokens are the tokenized words for the sentence
	probability = {}
	print(confusion_word_set)
	for candidate in confusion_word_set:
		temp_probability = 0
		if(term_frequency.get(candidate) != None and term_frequency.get(candidate) != 0):
			for i in range(INDEX-3, INDEX+3):
				if (0 <= i < len(tokens)):
					if(tokens[i] in relevant_words):
						if(context_words_dictionary.get(candidate) != None):
							if(context_words_dictionary.get(candidate).get(tokens[i]) != None):
								if(temp_probability == 0):
									temp_probability = 1.0*context_words_dictionary[candidate][tokens[i]]/term_frequency[candidate]
								else:
									temp_probability *= 1.0*context_words_dictionary[candidate][tokens[i]]/term_frequency[candidate]

			temp_probability *= term_frequency.get(candidate)
		probability[candidate] = temp_probability
	return probability


def fetch_trie():
	return Trie(dataPath + 'american-english')


def verifyInDict(word):
	results = trie.getCandidates(word, 0)
	if len(results) > 0:
		return True
	else:
		return False

# loading the data
editDistance = 2
# generating the trie
trie = fetch_trie()

inputPhrase = input('Enter input phrase: ')
faultyWords = []

initialTokens = inputPhrase.split(" ")
finalTokens = []
confusionSet = {}

for token in initialTokens:
	token = token.strip().lower()

	if verifyInDict(token) == False:
		subTokens = getSortedWords(token)
		falutyFlag = False

		for subT in subTokens:
			if verifyInDict(subT) == False and falutyFlag == False:
				falutyFlag = True

		if(falutyFlag == True):
			faultyWords.append((len(finalTokens), token))
			finalTokens.append(token)
			# confusionSet[token] = trie.getCandidates(token, 2)[0:6]
		else:
			for subT in subTokens:
				finalTokens.append(subT)
				# confusionSet[subT] = trie.getCandidates(subT, 2)[0:6]

	else:
		finalTokens.append(token)
		# confusionSet[token] = trie.getCandidates(token, 2)[0:6]


print('Prob:', probability_context_word(finalTokens[2], finalTokens, 2))

# print(finalTokens)
# print(confusionSet)