from collections import namedtuple


# def SaveDictionary(dictionary,File):
#     with open(datapath + File, "wb") as myFile:
#         pickle.dump(dictionary, myFile)
#         myFile.close()

##creating the dictionay(single time use) for co-occurances
# for key, value in sub_confusion.items():
#     corpus_co[key] = len(re.findall(r"\w"+key, data))
# text_file = open(datapath + "co_occurances.txt", "w")
# text_file.write("%s" % corpus_co)
# text_file.close()
 

##creating the dictionay(single time use) for single-occurances
# char_alphabet={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0,}
# for key, value in char_alphabet.items():
#     char_alphabet[key] = len(re.findall(r"\w"+key, data))
# text_file = open(datapath + "single_occurances.txt", "w")
# text_file.write("%s" % char_alphabet)
# text_file.close()


# #creating word frequency dictionary from word frequency text file 
# word_frq={}
# with open("../data/my_frq.txt", 'r', encoding="latin-1") as file:
#     word_frq = {}
#     for l in file:  
#         key,value = l.strip().split(' ')
#         # print(key+"  "+value)
#         if key in word_frq:
#             word_frq[key]=word_frq[key]+eval(value)
#         else:
#             word_frq[key]=eval(value)

# text_file = open("../data/word_frq.txt", "w")
# text_file.write("%s" % word_frq)
# text_file.close()

def levenshtein_edits(s, t):
    edits = namedtuple("edits", "error correction edit_Type")
    edit_list = [];
    m, n = len(s), len(t)
    d = [range(n+1)]
    # print d
    d += [[i] for i in range(1,m+1)]
    # print m
    for i in range(0,m):
        for j in range(0,n):
            cost = 1
            if s[i] == t[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, # deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
   
    # print d
    k = len(s)
    l = len(t)
    while((k>0) or (l>0)):
        if (k==0):
          temp_min = d[k][l-1]; x_flag=1
        elif (l==1 and k != 1):
          temp_min = d[k-1][l]; another_flag=1
          k = k-1
          # print "I came here"
          if not (edits(t[l-1],t[l-1]+s[k],"Addition") in edit_list) :
            edit_list.append(edits(t[l-1],t[l-1]+s[k],"Addition"))
        elif (k==1 and l != 1):
          temp_min = d[k][l-1]; another_flag_2=1
          l = l-1
          if not (edits(t[l-1:l+1],t[l-1],"Removal") in edit_list) :
                edit_list.append(edits(t[l-1:l+1],t[l-1],"Removal"))
        elif (l==0):
          temp_min = d[k-1][l]; y_flag=1
        else:
          temp_min = min(d[k-1][l],d[k][l-1],d[k-1][l-1]); x_flag=0; y_flag=0;another_flag=0;another_flag_2=0
        if (not (another_flag or another_flag_2)):
          if (temp_min == d[k-1][l-1]):
            if(s[k-1] == t[l-1]):
              k = k-1; l = l-1
            else :
              k = k-1; l = l-1
              if not (edits(t[l],s[k],"Substitution") in edit_list) :
                edit_list.append(edits(t[l],s[k],"Substitution"))
                # print "Printing from substitution"
                # print t[l]
                # print s
                # print s[k]
          elif (temp_min == d[k][l-1]):
            l = l-1
            if not (edits(t[l-1:l+1],t[l-1],"Removal") in edit_list) :
                edit_list.append(edits(t[l-1:l+1],t[l-1],"Removal"))
          else:
            k = k-1
            if not (edits(t[l-1],t[l-1]+s[k],"Addition") in edit_list) :
                edit_list.append(edits(t[l-1],t[l-1]+s[k],"Addition"))

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
                    if(r1 != 0): 
                        r1 = incorr[i]
                        r2 = candidate[i]
                    else: 
                        if(r1 != candidate[i]):
                            return(r1, r2, False)

            return (r1, r2, True)
        else:
            return (r1, r2, False)


# candidates=[{'word':'hello','del1':'ll','del2':0,'sub1':'la','sub2':0,'ins1':0,'ins2':0,'rev1':0,'rev2':0,'score':0},
#             {'word':'held','del1':0,'del2':0,'sub1':'od','sub2':0,'ins1':0,'ins2':0,'rev1':0,'rev2':0,'score':0}]

def get_bayesian_probabilities(incorr, suggestions):

    # the data directory relative to main folder
    datapath = './data/'

    # corpus data
    with open(datapath + 'corpus.txt', 'r') as myfile:
        data = myfile.read()


    # loading additon dictionary
    ins_confusion = []
    with open(datapath + 'ins_confusion.txt','r') as inf:
        for line in inf:
            ins_confusion = eval(line)

    # loading deletion dictionary
    del_confusion = []
    with open(datapath + 'del_confusion.txt', 'r') as inf:
        for line in inf:
            del_confusion = eval(line)

    # loading reversal dictionary
    rev_confusion = []
    with open(datapath + 'rev_confusion.txt', 'r') as inf:
        for line in inf:
            rev_confusion = eval(line)

    # loading substitution dictionary
    sub_confusion = []
    with open(datapath + 'sub_confusion.txt', 'r') as inf:
        for line in inf:
            sub_confusion = eval(line) 

    # co-occurances of two characters in corpus data
    corpus_co = []
    with open(datapath + 'co_occurances.txt', 'r') as inf:
        for line in inf:
            corpus_co = eval(line) 

    # single occurance of characters in corpus data
    corpus_single = []
    with open(datapath + 'single_occurances.txt', 'r') as inf:
        for line in inf:
            corpus_single = eval(line) 

    # loading word frequency dictionary from text file 
    word_frq = []
    with open(datapath + 'word_frq.txt', 'r') as inf:
        for line in inf:
            word_frq = eval(line)

    suggestions = [sugg.lower().replace("'", "") for sugg in suggestions]
    candidates = []

    for i in range(0, len(suggestions)):
        each_candi = {'word':0, 'del1':0, 'del2':0, 'sub1':0, 'sub2':0, 'ins1':0, 'ins2':0, 'rev1':0, 'rev2':0, 'score':0}
        each_candi['word'] = suggestions[i]

        detectReversal = detectSingleReversal(incorr, suggestions[i])
        if(detectReversal[2] == False):
            list = levenshtein_edits(incorr, suggestions[i])
        else:
            list = [[detectReversal[0], detectReversal[1], "Reversal"]]

        # for each error type in a word, looping through errors
        for j in range(len(list)):
            s = 0
            r = 0
            a = 0
            rev = 0

            if list[j][2] == 'Substitution':
                if s == 0:
                    each_candi['sub1'] = list[j][1] + list[j][0]
                    s = s + 1
                else:
                    if s == 1:
                        each_candi['sub2'] = list[j][0] + list[j][1]

            if list[j][2] == 'Removal':
                if r == 0:
                    each_candi['del1'] = list[j][0]
                    r = r + 1
                else:
                    if r == 1:
                        each_candi['del2'] = list[j][0]

            if list[j][2] == 'Addition':
                if a == 0:
                    each_candi['ins1'] = list[j][1]
                    a = a + 1
                else:
                    if a == 1:
                        each_candi['ins2'] = list[j][1]        

            if list[j][2] == 'Reversal':
                if a == 0:
                    each_candi['rev1'] = list[j][0]
                    a = a + 1
                else:
                    if a == 1:
                        each_candi['rev2'] = list[j][1]        


        candidates.append(each_candi)

    sum = 0
    for i in range(0, len(candidates)):

        if candidates[i]['del1'] != 0:
            del_score = del_confusion[candidates[i]['del1']]/(corpus_co[candidates[i]['del1']])
            if candidates[i]['del2'] != 0:
                del_score = del_score*del_confusion[candidates[i]['del2']]/(corpus_co[candidates[i]['del2']])
            # if(del_score == 0):
                # del_score += 0.5
        else:
            del_score = 1

        if candidates[i]['sub1'] != 0:
            sub_score = sub_confusion[candidates[i]['sub1']]/(corpus_single[candidates[i]['sub1'][1]])
            if candidates[i]['sub2'] != 0:
                sub_score = sub_score*sub_confusion[candidates[i]['sub2']]/(corpus_single[candidates[i]['sub2'][1]])
            # if(sub_score == 0):
                # sub_score += 0.5
        else:
            sub_score = 1

        if candidates[i]['ins1'] != 0:
            ins_score = ins_confusion[candidates[i]['ins1']]/(corpus_single[candidates[i]['ins1'][1]])
            if candidates[i]['ins2'] != 0:
                ins_score = ins_score*ins_confusion[candidates[i]['ins2']]/(corpus_single[candidates[i]['ins2'][1]])
            # if(ins_score == 0):
                # ins_score += 0.5
        else:
            ins_score = 1

        if candidates[i]['rev1'] != 0:
            rev_score = rev_confusion[candidates[i]['rev1']]/(corpus_co[candidates[i]['rev1']])
            if candidates[i]['rev2'] != 0:
                rev_score = rev_score*rev_confusion[candidates[i]['rev2']]/(corpus_co[candidates[i]['rev2']])
            # if(rev_score == 0):
                # rev_score += 0.5
        else:
            rev_score = 1

        # since some suggestions don't exist in corpus
        if(word_frq.get(candidates[i]['word']) != None):
            word_frq_smoothed = word_frq[candidates[i]['word']] + 0.5
        else:
            word_frq_smoothed = 0.5 + 0.5

        # print(candidates[i]['word'])
        # print(del_score, sub_score, ins_score, word_frq_smoothed)
        # print('')
        candidates[i]['score'] = del_score*sub_score*ins_score*word_frq_smoothed

        sum = sum + candidates[i]['score']

    probArray = []
    for candi in candidates:
        probArray.append(candi['score'])

    return probArray
