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

import pickle

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
        print('Generating the BK-Tree of the dictionary...')
        print('This might take a while...')

        self.distfn = distfn

        it = iter(words)
        root = next(it)
        self.tree = (root, {})

        for i in it:
            self._add_word(self.tree, i.lower())

        print('Successfully generated the BK-Tree of the given dictionary!')

    def _add_word(self, parent, word):
        pword, children = parent
        d = self.distfn(word, pword)
        # check if the new word is same as parent
        if d != 0:
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

# http://en.wikibooks.org/wiki/Algorithm_implementation/Strings/Levenshtein_distance#Python
def levenshtein(s, t):
    m, n = len(s), len(t)
    d = [range(n+1)]
    d += [[i] for i in range(1, m+1)]
    for i in range(0, m):
        for j in range(0, n):
            # gives 1 when true and 0 when false
            cost = t[i] != s[j]

            d[i+1].append(min(d[i][j+1]+1, # deletion
                           d[i+1][j]+1, #insertion
                           d[i][j]+cost) #substitution
                       )
    return d[m][n]

def levenshteinDP(s, t):
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

def dict_words(dictfile="./american-english"):
    # Return an iterator that produces words in the given dictionary.
    return filter(len, map(str.strip, open(dictfile)))
