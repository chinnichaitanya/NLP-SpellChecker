import os
import time
import pickle

from bin.bktemp import *
from bin.editex import *
from bin.bayesian import *

def fetch_bkTree_data():
	filepath = './data/data.bktreeTemp'
	if(os.path.isfile(filepath)):
		print('BK-Tree data already exists in the filepath. Loading it...')

		# bkTree = eval(open(filepath, 'r').read())
		bkTree_file = open(filepath, 'rb')
		bkTree = pickle.load(bkTree_file)		
		
		print('Done!')
		
		return bkTree
	else:
		print('BK-Tree data doesn\'t exist in the filepath.')

		bkTree = generateBKTree('./data/american-english')
		pickle.dump(bkTree, open(filepath, 'wb'))
		# treeFile = open(filepath, 'w')
		# treeFile.write(str(bkTree))
		# treeFile.close()

		return bkTree

# loading the data
editDistance = 2

t = time.time()
bkTree = fetch_bkTree_data()
timeBkTree = time.time() - t
print('Time taken to load the BK-Tree: ' + str(round(timeBkTree, 4)) + '\n')

# taking the incorrect word
incorrectWord = input('Please enter the incorrect word: ')

# generating the collection set for the given incorrect word
t = time.time()
collectionSet = getCandidates(bkTree, incorrectWord, editDistance)
timeCollectionSet = time.time() - t

# calculating the phonetic probability of candidates
t = time.time()
phoneticProbabilityArray = get_phonetic_probabilities(incorrectWord, collectionSet)
timePhoneticProbArray = time.time() - t
# calculating the bayesian porbability of candidates
t = time.time()
bayesianProbabilityArray = get_bayesian_probabilities(incorrectWord, collectionSet)
timeBayesianProbArray = time.time() - t

# calculating the total probability
t = time.time()
# totalProbabilityArray = [pow(pow(0.6*p, 2)+pow(0.4*b, 2), 0.5) for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
# totalProbabilityArray = [0.6*p+0.4*b for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
totalProbabilityArray = [p*b for p, b in zip(phoneticProbabilityArray, bayesianProbabilityArray)]
# totalProbabilityArray = [1*b for b in phoneticProbabilityArray]
tempSum = sum(totalProbabilityArray)
for i in range(0, len(collectionSet)):
	totalProbabilityArray[i] /= tempSum
timeTotalProbArray = time.time() - t
# generating the dictionary with the suggestions and total probability
t = time.time()
totalDict = []
for i in range(0, len(collectionSet)):
	totalDict.append((collectionSet[i], totalProbabilityArray[i]))
timeTotalDict = time.time() - t

t = time.time()
totalDict = sorted(totalDict, key=lambda x: x[1], reverse=True)
timeSortTotalDict = time.time() - t

print('\nBelow are the suggestions for the word: ' + incorrectWord + '\n')
print('Word\t\tProbability\t Rank')
print('~~~~\t\t~~~~~~~~~~~\t ~~~~')
for i in range(0, min(10, len(collectionSet))):
	print(str(totalDict[i][0]) + '\t\t' + str(round(100*totalDict[i][1], 2)) + '%\t\t Rank #' + str(i+1))

print('\n\n##### Times (in sec) ####')
print('Time for generating collection set:\t' + str(round(timeCollectionSet, 4)))
print('Time for generating phoneticProbArray:\t' + str(round(timePhoneticProbArray, 4)))
print('Time for generating bayesianProbArray:\t' + str(round(timeBayesianProbArray, 4)))
print('Time for generating totalProbArray:\t' + str(round(timeTotalProbArray, 4)))
print('Time for generating totalDict:\t\t' + str(round(timeTotalDict, 4)))
print('Time for sorting totalDict:\t\t' + str(round(timeSortTotalDict, 4)))
print('Total time for execution:\t\t' + str(round(timeBkTree+timeCollectionSet+timePhoneticProbArray+timeBayesianProbArray+timeTotalProbArray+timeTotalDict+timeSortTotalDict, 4)))
