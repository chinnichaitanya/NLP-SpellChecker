import time
# from numpy import *

def editexlettersCode(l1, l2):
	num = [0, 0]
	letters = [l1, l2]
	for index in [0, 1]:
		if(letters[index] == 'a' or letters[index] == 'e' or letters[index] == 'i' or letters[index] == 'o' or letters[index] == 'u' or letters[index] == 'y'):
			num[index] += pow(2, 9)
		if(letters[index] == 'b' or letters[index] == 'p'):
			num[index] += pow(2, 8)
		if(letters[index] == 'c' or letters[index] == 'k' or letters[index] == 'q'):
			num[index] += pow(2, 7)
		if(letters[index] == 'd' or letters[index] == 't'):
			num[index] += pow(2, 6)
		if(letters[index] == 'l' or letters[index] == 'r'):
			num[index] += pow(2, 5)
		if(letters[index] == 'm' or letters[index] == 'n'):
			num[index] += pow(2, 4)
		if(letters[index] == 'g' or letters[index] == 'j'):
			num[index] += pow(2, 3)
		if(letters[index] == 'f' or letters[index] == 'p' or letters[index] == 'v'):
			num[index] += pow(2, 2)
		if(letters[index] == 'x' or letters[index] == 's' or letters[index] == 'z'):
			num[index] += pow(2, 1)
		if(letters[index] == 'c' or letters[index] == 's' or letters[index] == 'z'):
			num[index] += pow(2, 0)
	if((num[0] & num[1]) > 0):
		return True
	else:
		return False


def d(a, b):
	if(a == b):
		return 0
	elif(editexlettersCode(a, b) or ((a == 'h' or a == 'w') and  a != b)):
		return 1
	else:
		return 2


def r(a, b):
	if(a == b):
		return 0
	elif(editexlettersCode(a, b)):
		return 1
	else:
		return 2

def editexDistance(s, t):
    m, n = len(s), len(t)
    memo = []
    for l in range(0, m):
    	temp = []
    	for k in range(0, n):
    		temp.append(0)
    	memo.append(temp)
    for i in range(0, m):
        for j in range(0, n):
            if(i==0 and j==0):
            	memo[i][j] = r(s[0], t[0])
            elif(j==0):
            	memo[i][j] = memo[i-1][j] + d(s[i-1], s[i])
            elif(i==0):
            	memo[i][j] = memo[i][j-1] + d(t[j-1], t[j])
            else:
            	memo[i][j] = min(memo[i-1][j]+d(s[i-1], s[i]),
                               memo[i][j-1]+d(t[j-1], t[j]), 
                               memo[i-1][j-1]+r(s[i], t[j]))
    return memo[m-1][n-1]


def editexDistance_2(m, n, wordOne, wordTwo):
	if(m == 0 and n == 0):
		return 0
	elif(n == 0):
		return editexDistance(m-1, 0, wordOne, wordTwo) + d(wordOne[m-1], wordOne[m])
	elif(m == 0):
		return editexDistance(0, n-1, wordOne, wordTwo) + d(wordTwo[n-1], wordTwo[n])
	else:
		distOne = editexDistance(m-1, n, wordOne, wordTwo) + d(wordOne[m-1], wordOne[m])
		distTwo = editexDistance(m, n-1, wordOne, wordTwo) + d(wordTwo[n-1], wordTwo[n])
		distThree = editexDistance(m-1, n-1, wordOne, wordTwo) + r(wordOne[m], wordTwo[n])
		tempArr = [distOne, distTwo, distThree]
		return min(tempArr)

def get_phonetic_probabilities(incorr, suggestions):

	dist = []
	wordOne = incorr.lower()
	wordTwo = ''

	for sugg in suggestions:
		wordTwo = sugg.lower()
		# t = time.time()
		val = editexDistance(wordOne, wordTwo)
		# val = editexDistance(len(wordOne)-1, len(wordTwo)-1, wordOne, wordTwo)
		# print(str(val) + ' - Time for "' + sugg + '" : ' + str(time.time()-t) + '\n')
		dist.append(val)

	tempProbArray = []
	for d in dist:
		tempProbArray.append(1/(d+0.5))

	sum_tempProbArray = sum(tempProbArray)
	probArray = []
	for p in tempProbArray:
		probArray.append(p/sum_tempProbArray)

	return probArray
