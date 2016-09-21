class Trie:
	def __init__(self, dictPath=None):
		self.wordAtNode = None
		self.children = {}

		if(dictPath != None):
			dictFile = open(dictPath, 'r').read().split()
			for word in dictFile:
				self.insertWord(word.lower().strip())


	def insertWord(self, newWord):
		trieNode = self
		for letter in newWord:
			if letter not in trieNode.children:
				trieNode.children[letter] = Trie()

			trieNode = trieNode.children[letter]

		trieNode.wordAtNode = newWord


	def getCandidates(self, searchWord, maxDistance):
		firstRow = range(0, len(searchWord)+1)
		candidates = []

		def search(trieNode, letter, firstRow):
			secondRow = [firstRow[0] + 1]
			for i in range(1, len(searchWord)+1):
            	# gives 1 when true and 0 when false
				cost = searchWord[i-1] != letter

				val = min(firstRow[i] + 1, firstRow[i-1] + cost, secondRow[i-1] + 1)
				secondRow.append(val)

			if(secondRow[-1] <= maxDistance and trieNode.wordAtNode != None):
				candidates.append(trieNode.wordAtNode)
			
			if(min(secondRow) <= maxDistance):
				for letter in trieNode.children:
					search(trieNode.children[letter], letter, secondRow)

		for letter in searchWord:
			if(letter in self.children):
				search(self.children.get(letter), letter, firstRow)

		return candidates

