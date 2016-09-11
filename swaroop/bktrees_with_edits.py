"""
This module implements Burkhard-Keller Trees (bk-tree).  bk-trees
allow fast lookup of words that lie within a specified distance of a
query word.  For example, this might be used by a spell checker to
find near matches to a mispelled word.
The implementation is based on the description in this article:
http://blog.notdot.net/2007/4/Damn-Cool-Algorithms-Part-1-BK-Trees
Licensed under the PSF license: http://www.python.org/psf/license/
- Adam Hupp <adam@hupp.org>
"""
from itertools import imap, ifilter
from collections import namedtuple

import pickle
import time
import sys

edits = namedtuple("edits", "error correction edit_Type")
edit_list = [];

class BKTree:
    def __init__(self, distfn, words):
        """
        Create a new BK-tree from the given distance function and
        words.
        
        Arguments:
        distfn: a binary function that returns the distance between
        two words.  Return value is a non-negative integer.  the
        distance function must be a metric space.
        
        words: an iterable.  produces values that can be passed to
        distfn
        
        """
        self.distfn = distfn

        it = iter(words)
        root = it.next()
        self.tree = (root, {})

        for i in it:
            self._add_word(self.tree, i)

    def _add_word(self, parent, word):
        pword, children = parent
        d = self.distfn(word, pword)
        if d in children:
            self._add_word(children[d], word)
        else:
            children[d] = (word, {})

    def query(self, word, n):
        """
        Return all words in the tree that are within a distance of `n'
        from `word`.  
        Arguments:
        
        word: a word to query on
        n: a non-negative integer that specifies the allowed distance
        from the query word.  
        
        Return value is a list of tuples (distance, word), sorted in
        ascending order of distance.
        
        """
        def rec(parent):
            pword, children = parent
            d = self.distfn(word, pword)
            results = []
            if d <= n:
                results.append( (d, pword) )
                
            for i in range(d-n, d+n+1):
                child = children.get(i)
                if child is not None:
                    results.extend(rec(child))
            return results

        # sort by distance
        return sorted(rec(self.tree))
    


def brute_query(word, words, distfn, n):
    """A brute force distance query
    Arguments:
    word: the word to query for
    words: a iterable that produces words to test
    distfn: a binary function that returns the distance between a
    `word' and an item in `words'.
    n: an integer that specifies the distance of a matching word
    
    """
    return [i for i in words
            if distfn(i, word) <= n]


def maxdepth(tree, count=0):
    _, children = t
    if len(children):
        return max(maxdepth(i, c+1) for i in children.values())
    else:
        return c


# http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
def levenshtein(s, t):
    m, n = len(s), len(t)
    d = [range(n+1)]
    d += [[i] for i in range(1,m+1)]
    for i in range(0,m):
        for j in range(0,n):
            cost = 1
            if s[i] == t[j]: cost = 0

            d[i+1].append( min(d[i][j+1]+1, # deletion
                               d[i+1][j]+1, #insertion
                               d[i][j]+cost) #substitution
                           )
    return d[m][n]

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
        if (not (x_flag or y_flag or another_flag or another_flag_2)):
          if (temp_min == d[k-1][l-1]):
            if(s[k-1] == t[l-1]):
              k = k-1; l = l-1
            else :
              k = k-1; l = l-1
              if not (edits(t[l],s[k],"Substitution") in edit_list) :
                edit_list.append(edits(t[l],s[k],"Substitution"))
          elif (temp_min == d[k][l-1]):
            l = l-1
            if not (edits(t[l-1:l+1],t[l-1],"Removal") in edit_list) :
                edit_list.append(edits(t[l-1:l+1],t[l-1],"Removal"))
          else:
            k = k-1
            if not (edits(t[l-1],t[l-1]+s[k],"Addition") in edit_list) :
                edit_list.append(edits(t[l-1],t[l-1]+s[k],"Addition"))
        else:
          if x_flag:
            print "x_flag was helpful!"
            l=l-1
            if not (edits(t[l-1:l+1],t[l-1],"Removal") in edit_list) :
                edit_list.append(edits(t[l-1:l+1],t[l-1],"Removal"))
          if y_flag:
            k = k-1
            print "y_flag was helpful!"         
    return edit_list

def dict_words(dictfile="/usr/share/dict/american-english"):
    "Return an iterator that produces words in the given dictionary."
    return ifilter(len,
                   imap(str.strip,
                        open(dictfile)))


def timeof(fn, *args):
    import time
    t = time.time()
    res = fn(*args)
    print "time: ", (time.time() - t)
    return res



if __name__ == "__main__":
    load_time = time.time()
pkl_file = open('save.p', 'rb')
tree =pickle.load(pkl_file)
   # pickle.dump( tree, open( "save.p", "wb" ) )
load_finish = time.time()
start = time.time()
candidates = tree.query("peases",2) 
print candidates

for candidate in candidates:
    candidate_edit_list = []
    candidate_edit_list = levenshtein_edits(candidate,"peases")
    print candidate_edit_list
end = time.time()
print end-start
print load_finish-load_time

