words = open('word_frq.txt', encoding='latin-1').read()
words = eval(words)

words = sorted(words.items(), key=lambda x:x[1], reverse=True)

string = ''
for wo in words:
	string += wo[0] + '\n'

file = open('up.txt', 'w')
file.write(string)