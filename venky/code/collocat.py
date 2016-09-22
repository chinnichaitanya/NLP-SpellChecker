import nltk
import time
import pickle

brown_words = nltk.corpus.brown.words()

collocate_words = {}

t = time.time()
print(len(brown_words))
# for i in range(0, len(brown_words)-2):
# 	if(collocate_words.get(brown_words[i]) == None):
# 		collocate_words[brown_words[i]] = {}
# 	if(collocate_words.get(brown_words[i+1]) == None):
# 		collocate_words[brown_words[i+1]] = {}
# 	if(collocate_words.get(brown_words[i+2]) == None):
# 		collocate_words[brown_words[i+2]] = {}
# 	text=brown_words[i]+brown_words[i+1]+brown_words[i+2]
# 	x=nltk.pos_tag(text)
# 	tag1=x[0][1]
# 	tag2=x[1][1]
# 	tag3=x[2][1]
# 	if(collocate_words.get(brown_words[i]).get(tag1+tag2+tag3)==None or 
# 		collocate_words.get(brown_words[i+1]).get(tag1+tag2+tag3)==None or
# 		collocate_words.get(brown_words[i+2]).get(tag1+tag2+tag3)==None):

# 		collocate_words.get(brown_words[i])[tag1+tag2+tag3]=1
# 		collocate_words.get(brown_words[i+1])[tag1+tag2+tag3]=1
# 		collocate_words.get(brown_words[i+2])[tag1+tag2+tag3]=1
# 	else:
# 		collocate_words.get(brown_words[i])[tag1+tag2+tag3]+=1
# 		collocate_words.get(brown_words[i+1])[tag1+tag2+tag3]+=1
# 		collocate_words.get(brown_words[i+2])[tag1+tag2+tag3]+=1

# 	print(collocate_words)

file = open('collocate_words.txt', 'w')
file.write(str(collocate_words))
file.close()

pi_file = open('collate_words.pickle', 'w')
pickle.dump(collocate_words, pi_file, protocol=2)

 # Done after time: 228.5378544330597
# print('Done after time:', time.time()-t)
