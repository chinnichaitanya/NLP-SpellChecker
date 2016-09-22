from collections import namedtuple
import operator

file_list = ["./data/substitution_matrix.txt", "./data/deletion_matrix.txt", "./data/insertion_matrix.txt", "./data/reversal_matrix.txt"]	
# Get the edits by putting levenshtein_edits(candidate_word, typo)
# bayesian_correction_probability(x,y,correction_type)
# Correction Type : 0:substitution, 1:deletion, 2:insertion, 3:reversal
bayesian_matrices = [[[0 for x in range(0,26)] for y in range(0,26)] for z in range(0,4)]	
i=0
for files in file_list:
	f = open(files, 'r')
	j = 0
	for line in f:
		if line.strip():
			char_integers = line.split()
			k=0
			for string in char_integers:
				bayesian_matrices[i][j][k] = int(string)
				k += 1
			j += 1
	i += 1

file_list = ["./data/co_occurances.txt","./data/single_occurances.txt","./data/word_frq.txt"]
i=0
for current_file in file_list:
	f= open(current_file,'r')
	for line in f:
		if(i==0):
			co_occurances = eval(line) 
		elif(i==1):
			single_occurances = eval(line)
		else:
			term_frequency = eval(line)
	i += 1

def bayesian_correction_probability(x,y,correction_type):
	if(str(x).isalpha() and str(y).isalpha()):	
		confusion_count = bayesian_matrices[correction_type][ord(x)-97][ord(y)-97]
		# print(x, y, correction_type, confusion_count)
		if(correction_type == 1 or correction_type == 3):
			if(co_occurances[x+y] != 0):
				if confusion_count != 0:
					return (1.0*confusion_count/co_occurances[x+y])
				else:
					return (1.0*0.1/co_occurances[x+y])
			else:
				error_flag = 1
		else:
			if(single_occurances[x]):
				if confusion_count != 0:
					return (1.0*confusion_count/single_occurances[x])
				else:
					return (1.0*0.1/single_occurances[x])
			else:
				error_flag = 1
		if(error_flag == 1):
			return 0
	else:
		return 0

edits = namedtuple("edits", "error correction edit_Type")
def levenshtein_edits(s, t):
	edits = namedtuple("edits", "error correction edit_Type")
	edit_list = [];
	m, n = len(s), len(t)
	d = [range(n+1)]
	d += [[i] for i in range(1, m+1)]
	for i in range(0,m):
		for j in range(0,n):
			cost = 1
			if s[i] == t[j]: cost = 0
			values = [d[i][j+1]+1, d[i+1][j]+1, d[i][j]+cost]
			min_index, min_value = min(enumerate(values), key=operator.itemgetter(1))

			d[i+1].append(min_value)

	k = len(s)
	l = len(t)
	while((k>0) or (l>0)):
		if (k==0):
			temp_min = d[k][l-1]; x_flag=1
		elif (l==1 and k != 1):
			temp_min = d[k-1][l]; another_flag=1
			k = k-1
		# if not (edits(t[l-1],t[l-1]+s[k],"Insertion") in edit_list) :
			edit_list.append(edits(t[l-1],s[k],2))
		elif (k==1 and l != 1):
			temp_min = d[k][l-1]; another_flag_2=1
			l = l-1
		# if not (edits(t[l-1:l+1],t[l-1],"Removal") in edit_list) :
			edit_list.append(edits(t[l-1],t[l],1))
		elif (l==0):
			temp_min = d[k-1][l]; y_flag=1
		else:
			temp_min = min(d[k-1][l],d[k][l-1],d[k-1][l-1]); x_flag=0; y_flag=0;another_flag=0;another_flag_2=0
		if (not (another_flag or another_flag_2)):
			if(temp_min == d[k-1][l-1]):
				if(s[k-1] == t[l-1]):
					k = k-1; l = l-1
				else:
					k = k-1; l = l-1
			# if not (edits(t[l],s[k],"Substitution") in edit_list) :
				edit_list.append(edits(t[l],s[k],0))
			elif(temp_min == d[k][l-1]):
				l = l-1
			# if not (edits(t[l-1:l+1],t[l-1],"Removal") in edit_list) :
				edit_list.append(edits(t[l-1],t[l],1))
			else:
				k = k-1
			# if not (edits(t[l-1],t[l-1]+s[k],"Insertion") in edit_list) :
				edit_list.append(edits(t[l-1],s[k],2))

	return edit_list

def detectSingleReversal(incorr, candidate):
	r1 = 0
	r2 = 0
	if(len(incorr) != len(candidate)):
		return (r1, r2, False)

	asciDiff = [ord(a)-ord(b) for a, b in zip(incorr, candidate)]

	sumOfAsciDiff = sum(asciDiff)
	absSumOfAsciDiff = sum([abs(num) for num in asciDiff])
	if(absSumOfAsciDiff == 0):
		return (r1, r2, False)
	else:
		if(sumOfAsciDiff == 0):
			for i in range(len(asciDiff)):
				if(asciDiff[i] != 0):
					if(r1 == 0): 
						r1 = (i, incorr[i])
						r2 = (i, candidate[i])
					else:
						if((r1[1] != candidate[i]) or (abs(r1[0]-i) > 1)):
							return(r1, r2, False)
			return (r1[1], r2[1], True)
		else:
			return (r1, r2, False)


def get_bayesian_probabilities(typo, candidates):
	candidate_ranks = []
	for candidate in candidates:
		reversal_detection = detectSingleReversal(typo,candidate)
		candidate_probability = 0
		if(reversal_detection[2] == False): 
			candidate_edits_list = levenshtein_edits(candidate, typo)
			for each_edit in candidate_edits_list:
				if(candidate_probability == 0):
					candidate_probability = 1.0*bayesian_correction_probability(each_edit.error,each_edit.correction,each_edit.edit_Type)
				else:
					candidate_probability *= bayesian_correction_probability(each_edit.error,each_edit.correction,each_edit.edit_Type)
			# print(candidate, candidate_probability)

		else:
			candidate_probability = bayesian_correction_probability(reversal_detection[1],reversal_detection[0],2)

		if(term_frequency.get(candidate) != None):
			term_count = term_frequency[candidate]
		else:
			term_count = 5

		candidate_probability *= term_count
		candidate_ranks.append(candidate_probability)

	# Normalize the obtained probabilies 
	# factor=1.0/sum(candidate_ranks.values())
	# for k in candidate_ranks:
	# 	candidate_ranks[k] = candidate_ranks[k]*factor
	return candidate_ranks

# print bayesian_correction_probability('a','b',2)
# print bayesian_correction_probability('a','b',2)
# print bayesian_correction_probability('a','b',2)
# print bayesian_correction_probability('a','b',2)
# print bayesian_correction_probability('a','b',2)
