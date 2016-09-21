import time
import pickle
import sys

DICTIONARY = './american-english'
MAX_DIST = int(sys.argv[1])
TARGET = sys.argv[2]

NodeCount = 0
WordCount = 0

class TrieNode:
	def __init__(self):
		self.word = None
		self.children = {}

		global NodeCount
		NodeCount += 1

	def insert(self, word):
		node = self
		for letter in word:
			if letter not in node.children:
				node.children[letter] = TrieNode()

			node = node.children[letter]

		node.word = word

start = time.time()
trie = TrieNode()
for word in open(DICTIONARY, 'rt').read().split():
	WordCount += 1
	trie.insert(word)
# generation at runtime time = 0.841981

# unpickling time = 0.937603
trieGenerationTime = time.time() - start

# Read 119095 words into 272648 nodes in 0.822751 time
# print('Read %d words into %d nodes in %g time' %(WordCount, NodeCount, end-start))

def searchRecursive(node, letter, word, previousRow, results, maxCost):
	columns = len(word) + 1
	currentRow = [previousRow[0] + 1]

	for column in range(1, columns):
		insertCost = currentRow[column - 1] + 1
		deleteCost = previousRow[column] + 1

		if(word[column -1] != letter):
			replaceCost = previousRow[column - 1] + 1
		else:
			replaceCost = previousRow[column - 1]

		currentRow.append(min(insertCost, deleteCost, replaceCost))

	if(currentRow[-1] <= maxCost and node.word != None):
		results.append((node.word, currentRow[-1]))
	if(min(currentRow) <= maxCost):
		for letter in node.children:
			searchRecursive(node.children[letter], letter, word, currentRow, results, maxCost)


def search(word, maxCost):
	currentRow = range(len(word) + 1)
	results = []

	for letter in trie.children:
		searchRecursive(trie.children[letter], letter, word, currentRow, results, maxCost)

	return results

start = time.time()
results = search(TARGET, MAX_DIST)
searchTime = time.time() - start

for result in results:
	print(result)

print('Trie generation took: %g seconds' %(trieGenerationTime))
print('Search took: %g seconds' %(searchTime)) 
print('Total time: %g seconds' %(searchTime + trieGenerationTime)) 