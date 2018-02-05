
#
# Simple FASTA-reading library
# Copyright 2010 Kevin Kelley <kelleyk@kelleyk.net>
#
# Provided under the MIT license: yours gratis,
# and if it breaks, you get to keep both pieces.
#

import unittest

# An iterator that returns the nucleotide sequence stored in the given FASTA file.
class FastaSequence:
    def __init__(self, filename):
        self.f = open(filename, 'r')
        self.buf = ''
        self.info = self.f.readline()
        self.pos = 0
    def __iter__(self):
        return self
    def next(self):
        while '' == self.buf:
            self.buf = self.f.readline()
            if '' == self.buf:
                self.f.close()
                raise StopIteration
            self.buf = self.buf.strip()
        nextchar = self.buf[0]
        self.buf = self.buf[1:]
        self.pos += 1
        return nextchar

def getSequenceLength(filename):
    seq = FastaSequence(filename)
    n = 0
    for x in seq:
        n += 1
    return n

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

# Simple sanity checks
class TestKFASTA(unittest.TestCase):
    def test_readseq(self):
        seq = FastaSequence('trivial.fa')
        seqstr = ''
        for c in seq:
            seqstr += c
        self.assertTrue('ABCDEFGHIJKLMNOPQRSTUVWXYZ' == seqstr)
    def test_subseq(self):
        seq = FastaSequence('trivial.fa')
        i = 0
        for subseq in subsequences(seq, 3):
            print subseq
            i += 1
        self.assertTrue(24 == i)

class Container(object):
    def __init__(self, sequence, hashValue):
        self.s = sequence
        self.h = hashValue

def subsequenceHashes(seq, k):
    sequences = subsequences(seq, k)
    alphapet = 26
    #calculate first hash
    firstSeqence = sequences.next()
    firstLetter = firstSeqence[0]
    lastLetter = firstSeqence[len(firstSeqence) - 1]
    h = 0
    for x in range(0, k - 1):
        h += ord(c) * pow(alphapet, k - x - 1)
    info = Container(firstSeqence, h)
    yield info
    #loop over the sequence and hash
    for s in sequences:
        lastLetter = s[k - 1]
        #remove the first letter value
        h -= ord(firstLetter) * pow(alphapet, k - 1)
        h = h * alphapet
        #add the new letter value
        h += ord(lastLetter)
        firstLetter = s[0]
        info = Container(s, h)
        yield info

class MultiDict(object):
    def __init__(self):
        self.dict = {}
    
    def put(key, value):
        try:
            self.dict[key] = self.dict[key].append(value)
        except KeyError:
            self.dict[key] = []
            self.dict[key] = self.dict[key].append(value)
    def get(key):
        try:
            return self.dict[key]
        except KeyError:
            self.dict[key] = []
            return  self.dict[key]
    def deleteKey(key):
        try:
            del self.dict[key]
        except KeyError:
            pass

#if __name__ == '__main__':
#    unittest.main()