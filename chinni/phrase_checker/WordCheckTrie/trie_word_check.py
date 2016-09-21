import pickle
import time

from bin.trie import *
from bin.editex import *
from bin.bayesian import *

def fetch_trie():
	return Trie('./data/american-english')

# loading the data
editDistance = 2

trie = fetch_trie()
conf_set = {}

def getList(incorrectWord):
	# generating the collection set for the given incorrect word
	collectionSet = trie.getCandidates(incorrectWord, editDistance)

	# calculating the phonetic probability of candidates
	phoneticProbabilityArray = get_phonetic_probabilities(incorrectWord, collectionSet)
	# calculating the bayesian porbability of candidates
	bayesianProbabilityArray = get_bayesian_probabilities(incorrectWord, collectionSet)

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
	return totalDict[0:6]

t = time.time()
print('Starting...')
am_dict = open('./data/american-english', 'r').read().split()
for word in am_dict:
	word = word.strip().lower().replace("'", "")
	if(conf_set.get(word) == None):
		local_set = getList(word)
		conf_set[word] = local_set

dump_file = open('./dict_conf_set.pickle', 'w')
pickle.dump(conf_set, dump_file, protocol=2)

print('Done after time:', time.time.time()-t)
