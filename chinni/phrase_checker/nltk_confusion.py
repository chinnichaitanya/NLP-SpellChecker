# import nltk
# import time

# brown_words = nltk.corpus.brown.words()

# context_words = {}
# window = [-3, -2, -1, 1, 2, 3]

# t = time.time()
# for i in range(0, len(brown_words)):
# 	if(context_words.get(brown_words[i]) == None):
# 		context_words[brown_words[i]] = {}

# 	for k in window:
# 		if(i+k >= 0 and i+k <= len(brown_words)-1):
# 			if context_words.get(brown_words[i]).get(brown_words[i+k]) == None:
# 				context_words.get(brown_words[i])[brown_words[i+k]] = 1
# 			else:
# 				context_words.get(brown_words[i])[brown_words[i+k]] += 1

# file = open('context_words.txt', 'w')
# file.write(str(context_words))
# file.close()
# # Done after time: 228.5378544330597
# print('Done after time:', time.time()-t)














# import pickle
# cWords = eval(open('context_words.txt', 'r').read())
# pickle.dump(cWords, open('context_words.pickle', 'wb'))







import pickle
import time

t = time.time()

cfile = open('context_words.pickle', 'rb')
cWords = pickle.load(cfile)

print('Time taken:', time.time()-t)

print('Among[two]:', cWords.get('among', 'No word between').get('two', 0))
print('Between[two]:', cWords.get('between', 'No word between').get('two', 0))

print('Among[three]:', cWords.get('among', 'No word between').get('three', 0))
print('Between[three]:', cWords.get('between', 'No word between').get('three', 0))

