import re
import json

def SaveDictionary(dictionary,File):
    with open(File, "wb") as myFile:
        pickle.dump(dictionary, myFile)
        myFile.close()

##corpus data
with open('corpus.txt', 'r') as myfile:
    data=myfile.read()


#loading additon dictionary
ins_confusion = []
with open('ins_confusion.txt','r') as inf:
    for line in inf:
        ins_confusion = eval(line)
# print(ins_confusion["ac"])

#loading deletion dictionary
del_confusion = []
with open('del_confusion.txt','r') as inf:
    for line in inf:
        del_confusion = eval(line)
# print(del_confusion[0]["gw"])

#loading reversal dictionary
rev_confusion = []
with open('rev_confusion.txt','r') as inf:
    for line in inf:
        rev_confusion = eval(line)
# print(rev_confusion[0]["gw"])

#loading substitution dictionary
sub_confusion = []
with open('sub_confusion.txt','r') as inf:
    for line in inf:
        sub_confusion =eval(line) 
# print(sub_confusion)

#co-occurances of two characters in corpus data
corpus_co = []
with open('co_occurances.txt','r') as inf:
    for line in inf:
        corpus_co =eval(line) 
# print(corpus_co["gw"])

##creating the dictionay(single time use) for co-occurances
# for key, value in sub_confusion.items():
#     corpus_co[key] = len(re.findall(r"\w"+key, data))
# text_file = open("co_occurances.txt", "w")
# text_file.write("%s" % corpus_co)
# text_file.close()

#single occurance of characters in corpus data
corpus_single = []
with open('single_occurances.txt','r') as inf:
    for line in inf:
        corpus_single =eval(line) 

##creating the dictionay(single time use) for single-occurances
# char_alphabet={'a':0,'b':0,'c':0,'d':0,'e':0,'f':0,'g':0,'h':0,'i':0,'j':0,'k':0,'l':0,'m':0,'n':0,'o':0,'p':0,'q':0,'r':0,'s':0,'t':0,'u':0,'v':0,'w':0,'x':0,'y':0,'z':0,}
# for key, value in char_alphabet.items():
#     char_alphabet[key] = len(re.findall(r"\w"+key, data))
# text_file = open("single_occurances.txt", "w")
# text_file.write("%s" % char_alphabet)
# text_file.close()

############## testing
# dic={'hi':12,'fe':3,'ui':12}

# for key, value in dic.items():
#     print(key)
#     print(dic[key])
# print(dic)
##############

##creating word frequency dictionary from word frequency text file 
# word_frq={}
# with open("my_frq.txt", 'r') as file:
#     word_frq = {}
#     for l in file:  
#         key,value = l.strip().split(' ')
#         # print(key+"  "+value)
#         if key in word_frq:
#             word_frq[key]=word_frq[key]+eval(value)
#         else:
#             word_frq[key]=eval(value)

# text_file = open("word_frq.txt", "w")
# text_file.write("%s" % word_frq)
# text_file.close()

##loading word frequency dictionary from text file 
word_frq = []
with open('word_frq.txt','r') as inf:
    for line in inf:
        word_frq =eval(line) 

candidates=[{'word':'hello','del1':'ll','del2':0,'sub1':0,'sub2':0,'ins1':0,'ins2':0,'rev1':0,'rev2':0,'score':0},
            {'word':'held','del1':0,'del2':0,'sub1':'od','sub2':0,'ins1':0,'ins2':0,'rev1':0,'rev2':0,'score':0}]

# print(corpus_single[candidates[i]['sub1'][1]])
# print(word_frq[candidates[0]['word']])

sum=0
for i in range(len(candidates)):

    if candidates[i]['del1']!=0:
        del_score=del_confusion[candidates[i]['del1']]/(corpus_co[candidates[i]['del1']])
        if candidates[i]['del2']!=0:
            del_score=del_score*del_confusion[candidates[i]['del2']]/(corpus_co[candidates[i]['del2']])
    else:
        del_score=1

    if candidates[i]['sub1']!=0:
        sub_score=sub_confusion[candidates[i]['sub1']]/(corpus_single[candidates[i]['sub1'][1]])
        if candidates[i]['sub2']!=0:
            sub_score=sub_score*sub_confusion[candidates[i]['sub2']]/(corpus_single[candidates[i]['sub2'][1]])
    else:
        sub_score=1

    if candidates[i]['ins1']!=0:
        ins_score=ins_confusion[candidates[i]['ins1']]/(corpus_single[candidates[i]['ins1'][1]])
        if candidates[i]['ins2']!=0:
            ins_score=ins_score*ins_confusion[candidates[i]['ins2']]/(corpus_single[candidates[i]['ins2'][1]])
    else:
        ins_score=1

    if candidates[i]['rev1']!=0:
        rev_score=rev_confusion[candidates[i]['rev1']]/(corpus_co[candidates[i]['rev1']])
        if candidates[i]['rev2']!=0:
            rev_score=rev_score*rev_confusion[candidates[i]['rev2']]/(corpus_co[candidates[i]['rev2']])
    else:
        rev_score=1

    candidates[i]['score']=del_score*sub_score*ins_score*word_frq[candidates[i]['word']]

    sum=sum+candidates[i]['score']


for i in range(len(candidates)):
    print(candidates[i]['word'],candidates[i]['score']/sum*100)