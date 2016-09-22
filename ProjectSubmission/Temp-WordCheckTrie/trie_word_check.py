from bin.trie import *
from bin.editex import *
from bin.bayesian import *

def fetch_trie():
	return Trie('./data/american-english')

# loading the data
editDistance = 2

trie = fetch_trie()

# taking the incorrect word
input_file = open('word_input.txt', 'r').read().split()

final_answer = ''
for incorrectWord in input_file:
	final_answer += incorrectWord
	# generating the collection set for the given incorrect word
	collectionSet = trie.getCandidates(incorrectWord, editDistance)
	if(len(collectionSet) == 0):
		editDistance += 1
		collectionSet = trie.getCandidates(incorrectWord, editDistance)

	# calculating the phonetic probability of candidates
	phoneticProbabilityArray = get_phonetic_probabilities(incorrectWord, collectionSet)
	# calculating the bayesian porbability of candidates
	bayesianProbabilityArray = get_bayesian_probabilities(incorrectWord, collectionSet)

	# calculating the total probability
	# totalProbabilityArray = [pow(pow(0.6*p, 2)+pow(0.4*b, 2), 0.5) for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
	# totalProbabilityArray = [0.6*p+0.4*b for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
	totalProbabilityArray = [p*b for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
	# totalProbabilityArray = [1*b for b in phoneticProbabilityArray]
	tempSum = sum(totalProbabilityArray)
	for i in range(0, len(collectionSet)):
		totalProbabilityArray[i] /= tempSum
	# generating the dictionary with the suggestions and total probability
	totalDict = []
	for i in range(0, len(collectionSet)):
		totalDict.append((collectionSet[i], totalProbabilityArray[i]))

	totalDict = sorted(totalDict, key=lambda x: x[1], reverse=True)

	# print('\nBelow are the suggestions for the word: ' + incorrectWord + '\n')
	# print('Word\t\tProbability\t Rank')
	# print('~~~~\t\t~~~~~~~~~~~\t ~~~~')
	for i in range(0, min(10, len(collectionSet))):
		final_answer += '\t' + str(totalDict[i][0])
		final_answer += '\t' + str(round(100*totalDict[i][1], 2))
		# print(str(totalDict[i][0]) + '\t\t' + str(round(100*totalDict[i][1], 2)) + '%\t\t Rank #' + str(i+1))
	final_answer += '\n'

out_file = open('word_output.txt', 'w')
out_file.write(final_answer)
out_file.close()