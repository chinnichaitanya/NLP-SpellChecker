def generateBKTree(dictPath):

	print('Generating the BK-Tree of the dictionary...')
	print('This might take a while...')

	def insertWord(parentNode, newWord):
		parentWord = parentNode[0]
		childrenWords = parentNode[1]
		levDistance = levenshtein(newWord, parentWord)
	    # check if the new word is same as parent
		if(levDistance != 0):
			# if(childrenWords.get(levDistance) != None):
			if levDistance in childrenWords:
			 	insertWord(childrenWords[levDistance], newWord)
			else:
		 		childrenWords[levDistance] = (newWord, {})

	dictWords = open(dictPath).read().split()
	root = dictWords[0]

	tree = (root, {})
	for word in dictWords:
		insertWord(tree, word.lower().strip())

	print('Successfully generated the BK-Tree of the given dictionary!')

	return tree


def levenshtein(s, t):
    m, n = len(s), len(t)
    firstRow = range(0, m+1)
    secondRow = [1]
    for i in range(0, n):
        for j in range(0, m):
            # gives 1 when true and 0 when false
            cost = t[i] != s[j]

            val = min(secondRow[j]+1, firstRow[j+1]+1, firstRow[j]+cost)
            secondRow.append(val)

        firstRow = secondRow
        secondRow = [i+2]
    return firstRow[m]


def getCandidates(tree, searchWord, maxDistance):
	def search(parentNode):
		parentWord = parentNode[0]
		childrenWords = parentNode[1]
		candidates = []

		levDistance = levenshtein(searchWord, parentWord)
		if(levDistance <= maxDistance):
			candidates.append(parentWord)

		for i in range(abs(levDistance-maxDistance), levDistance+maxDistance+1):
			child = childrenWords.get(i)
			if(child != None):
				candidates.extend(search(child))
		return candidates

	wordSet = search(tree)
	return wordSet
