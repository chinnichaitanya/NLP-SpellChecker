import time

from bin.trie import *
from bin.editex import *
from bin.bayesian import *
from bin.stringTokenize import *

def fetch_trie():
	return Trie('./data/american-english')


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
			confusionSet[token] = trie.getCandidates(token, 2)[0:6]
		else:
			for subT in subTokens:
				finalTokens.append(subT)
				confusionSet[subT] = trie.getCandidates(subT, 2)[0:6]

	else:
		finalTokens.append(token)
		confusionSet[token] = trie.getCandidates(token, 2)[0:6]

print(finalTokens)
print(confusionSet)