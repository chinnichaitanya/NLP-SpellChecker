import time
import pickle
import nltk
import operator

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

coll_dict = {}
coll_dict = eval(open(dataPath + 'collocate_words_1.txt', 'rb').read())

# pkl_file_1 = open(dataPath + 'special_confusion_words.p', 'rb')
# confusion_sets = pickle.load(pkl_file_1)

confusion_sets = eval(open(dataPath + 'awesome_set.txt', 'rb').read())

# Here, "their" is the target word from the sentence. Replace it with a variable target word in a loop which iterates over each token generated from the sentence

def probability_context_word(target, tokens, INDEX):
	# tokens[INDEX]=target, where tokens is the array obtained from the output of tokenization algorithm.
	confusion_word_set = confusion_sets.get(target, [])

	for i in range(0,len(confusion_word_set)):
		confusion_word_set[i] = confusion_word_set[i].strip()


	# For every neigbour arrangement, find tags from nltk
	# For every tag arragment, search collocations dictionary
	# Average over each confusion word, if average is zero, give it some delta value
	# Multiply with the probability of context words
	# Choose max
	
	confusion_word_set.append(target)

	context_words = {}
	# Iterate over each word in confusion and take different neighbour arrangements
	for word in confusion_word_set:
		temp = context_words_dictionary.get(word, {})
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
	for candidate in confusion_word_set:
		temp_probability = 0
		if(term_frequency.get(candidate) != None and term_frequency.get(candidate) != 0):
			for i in range(INDEX-3, INDEX+3):
				if (0 <= i < len(tokens)):
					if(tokens[i] in relevant_words):
						if(context_words_dictionary.get(candidate) != None):
							if(context_words_dictionary.get(candidate).get(tokens[i]) != None 
								and context_words_dictionary.get(candidate).get(tokens[i]) != 0):
								# print ("place 1")
								x = context_words_dictionary.get(candidate).get(tokens[i])
							else:
								# print ("place 2")
								x = 5
							if(temp_probability == 0):
								# print ("place 3")
								temp_probability = x
							else:
								# print ("place 3")
								temp_probability *= x
			temp_probability *= term_frequency.get(candidate)
		else:
			# print ("place 4")
			temp_probability = 0.1

		pos = []
		for i in [-1,0,1]:
			if((0 <= INDEX+i-1 < len(tokens)) and (0 <= INDEX+i+1 < len(tokens))):
				z = nltk.pos_tag(tokens[INDEX+i-1]+' '+tokens[INDEX+i]+' '+tokens[INDEX+i+1])
				pos.append(z[0][1]+z[1][1]+z[2][1])
		post_score = 0
		for i in range(0, len(pos)):
			post_score += (1.0*int(coll_dict[target].get(pos[i], 0)))/len(pos)
		if(post_score == 0):
			post_score = 0.1
			# To be changed					
		temp_probability *= post_score
		probability[candidate] = temp_probability
	return probability

def fetch_trie():
	return Trie(dataPath + 'american_english_laga_unna_brown_corpus.txt')


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
global_flag_false = False
false_index = -1

inputPhrase = input('Enter input phrase: ')
faultyWords = {}

initialTokens = inputPhrase.split(" ")
finalTokens = []
confusionSet = {}

for i in range(0, len(initialTokens)):
	token = initialTokens[i].strip().lower()

	if verifyInDict(token) == False:
		subTokens = getSortedWords(token)
		falutyFlag = False

		for subT in subTokens:
			if verifyInDict(subT) == False and falutyFlag == False:
				falutyFlag = True

		if(falutyFlag == True):
			faultyWords[i] = token
			global_flag_false = True
			false_index = i
			finalTokens.append(token)
			# confusionSet[token] = trie.getCandidates(token, 2)[0:6]
		else:
			for subT in subTokens:
				finalTokens.append(subT)
				# confusionSet[subT] = trie.getCandidates(subT, 2)[0:6]

	else:
		finalTokens.append(token)
		# confusionSet[token] = trie.getCandidates(token, 2)[0:6]

falutyFlag = False
final_answer = ''
sorted_ans_dict = []
if global_flag_false == False:
	for i in range(0, len(finalTokens)):
		if(confusion_sets.get(finalTokens[i]) != None):
			# print('Prob:', probability_context_word(finalTokens[i], finalTokens,i))
			# final_answer += max(probability_context_word(finalTokens[i], finalTokens, i).items(), key=operator.itemgetter(1))[0]+' '
			ans_dict = probability_context_word(finalTokens[i], finalTokens, i)
			ans_dict = sorted(ans_dict.items(), key=operator.itemgetter(1), reverse=True)

			key, value = ans_dict.popitem()
			sorted_ans_dict.append((value, key, i))

			key, value = ans_dict.popitem()
			sorted_ans_dict.append((value, key, i))

			key, value = ans_dict.popitem()
			sorted_ans_dict.append((value, key, i))

	sorted_ans_dict = sorted(sorted_ans_dict, key=lambda x: x[0], reverse=True)
	final_replacement_key = sorted_ans_dict[0][2]

	final_answer = finalTokens[final_replacement_key]
	for someTup in sorted_ans_dict:
		if someTup[2] == final_replacement_key:
			final_answer += '\t' + someTup[1] + '\t' + str(someTup[0])
	final_answer += '\n'

else:
	targetCandidates = trie.getCandidates(finalTokens[false_index], 2)
	phoneticProbabilityArray = get_phonetic_probabilities(finalTokens[false_index], targetCandidates)
	bayesianProbabilityArray = get_bayesian_probabilities(finalTokens[false_index], targetCandidates)
	# totalProbabilityArray = [p for p in phoneticProbabilityArray]
	totalProbabilityArray = [p*b for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]

	totalDict = []
	for j in range(0, len(targetCandidates)):
		totalDict.append((targetCandidates[j], totalProbabilityArray[j]))

	totalDict = sorted(totalDict, key=lambda x: x[1], reverse=True)

	for k in range(0,false_index):
		final_answer += finalTokens[k]+' '

	final_answer = finalTokens[false_index]
	for iWrong in range(0, 3):
		final_answer += '\t' + totalDict[iWrong][0] + '\t' + str(totalDict[iWrong][1])
	final_answer += '\n'

print(final_answer)

# # print('Prob:', probability_context_word(finalTokens[2], finalTokens, 2))
# print(final_answer)

# print(finalTokens)
# print(faultyWords)