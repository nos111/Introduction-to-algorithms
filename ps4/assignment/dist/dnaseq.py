#!/usr/bin/env python2.7

import unittest
from dnaseqlib import *

### Utility classes ###

# Maps integer keys to a set of arbitrary values.
class Multidict:
    # Initializes a new multi-value dictionary, and adds any key-value
    # 2-tuples in the iterable sequence pairs to the data structure.
    def __init__(self, pairs=[]):
        self.dict = {}
        for p in pairs:
            self.put(p[0], p[1])
    # Associates the value v with the key k.
    def put(self, key, value):
        try:
            self.dict[key].append(value)
        except (AttributeError, KeyError):
            self.dict[key] = []
            self.dict[key].append(value)
    # Gets any values that have been associated with the key k; or, if
    # none have been, returns an empty sequence.
    def get(self, key):
        try:
            return self.dict[key]
        except KeyError:
            self.dict[key] = []
            return  self.dict[key]

# Given a sequence of nucleotides, return all k-length subsequences
# and their hashes.  (What else do you need to know about each
# subsequence?)
# Returns all subsequences of length k in seq.
def subsequences(seq, k):
    try:
        subseq = ''
        while True:
            while len(subseq) < k:
                subseq += seq.next()
            yield subseq
            subseq = subseq[1:]
    except StopIteration:
        return

class Container(object):
    def __init__(self, sequence, hashValue, begin):
        self.s = sequence
        self.h = hashValue
        self.begin = begin

class RollingHash(object):
    def __init__(self, text):
        self.alphapet = 26
        self.firstLetter = text[0]
        self.lastLetter = text[len(text) - 1]
        self.h = 0
        self.length = len(text)
        for x in range(0, self.length):
            self.h = self.h + ord(text[x]) * pow(self.alphapet, self.length - x - 1)
            #print "the hash value currently  is ", self.h
        #print "the hash value is ", self.h
    def slide(self, firstLetter, lastLetter):
        self.h -= ord(firstLetter) * pow(self.alphapet, self.length - 1)
        #print "the removed letter value is ", ord(firstLetter)
        self.h = self.h * self.alphapet
        self.h += ord(lastLetter)
        #print "the new hash value is ", self.h
    def current_hash(self):
        return self.h

def subsequenceHashes(seq, k):
    sequences = subsequences(seq, k)
    text = sequences.next()
    rh1 = RollingHash(text)
    firstLetter = text[0]
    index = 0
    yield (rh1.current_hash(), (text,index))
    for s in sequences:
        lastLetter = s[k - 1]
        #remove the first letter value
        rh1.slide(firstLetter, lastLetter)
        firstLetter = s[0]
        index += 1
        yield (rh1.current_hash(), (s,index))
    return


# Similar to subsequenceHashes(), but returns one k-length subsequence
# every m nucleotides.  (This will be useful when you try to use two
# whole data files.)
def intervalSubsequenceHashes(seq, k, m):
    raise Exception("Not implemented!")

# Searches for commonalities between sequences a and b by comparing
# subsequences of length k.  The sequences a and b should be iterators
# that return nucleotides.  The table is built by computing one hash
# every m nucleotides (for m >= k).
def getExactSubmatches(a, b, k, m):
    multiA = Multidict(subsequenceHashes(a, k))
    for hashValue, (text, pos) in subsequenceHashes(b, k):
        l = multiA.get(hashValue)
        for item in l:
            if item[0] == text:
                
                yield (item[1], pos)
    return

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print 'Usage: {0} [file_a.fa] [file_b.fa] [output.png]'.format(sys.argv[0])
        sys.exit(1)

    # The arguments are, in order: 1) Your getExactSubmatches
    # function, 2) the filename to which the image should be written,
    # 3) a tuple giving the width and height of the image, 4) the
    # filename of sequence A, 5) the filename of sequence B, 6) k, the
    # subsequence size, and 7) m, the sampling interval for sequence
    # A.
    compareSequences(getExactSubmatches, sys.argv[3], (500,500), sys.argv[1], sys.argv[2], 8, 100)
