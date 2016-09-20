from math import log

# Build a cost dictionary, assuming Zipf's law and cost = -math.log(probability).
sortedWords = open("sorted_words_with_freq.txt").read().split()
sortedWordsWithCost = dict((k, log((i+1)*log(len(sortedWords)))) for i, k in enumerate(sortedWords))
maxWordLength = max(len(x) for x in sortedWords)

def getSplitWithMinCost(i, s, cost):
    candidates = enumerate(reversed(cost[min(0, maxWordLength-i):i]))
    return min((c + sortedWordsWithCost.get(s[i-k-1:i], 9e999), k+1) for k, c in candidates)

def getsortedWords(s):
    """Uses dynamic programming to infer the location of spaces in a string
    withsplitsortedWords spaces."""

    # Find the best match for the i first characters, assuming cost has
    # been built for the i-1 first characters.
    # Returns a pair (match_cost, match_length).

    # Build the cost array.
    cost = [0]
    for i in range(1, len(s)+1):
        c, k = getSplitWithMinCost(i, s, cost)
        cost.append(c)

    # Backtrack to recover the minimal-cost string.
    splitsortedWords = []
    i = len(s)
    while i>0:
        c, k = getSplitWithMinCost(i, s, cost)
        splitsortedWords.append(s[i-k:i])
        i -= k

    return list(reversed(splitsortedWords))

inputString = input('Enter the phrase: ')
print(getsortedWords(inputString))