#!/usr/bin/env python
# encoding: utf-8

from itertools import groupby
from operator import itemgetter
import sys

def readMapOutput(file):
    for line in file:
        yield line.strip().split('\t')

def main(minSup):
    data = readMapOutput(sys.stdin)
    for currentName, group in groupby(data, itemgetter(0)):
        localDic = {}
        try:
            for currentName, conPatItems in group:
                conPatItems = conPatItems.strip().strip('[').strip(']')
                # print "%s\t%s" % (currentName, conPatItems)
                itemList = conPatItems.split(', ')
                for item in itemList:
                    item = item.strip().strip("'")
                    item = int(item)
                    localDic[item] = localDic.get(item, 0) + 1
                    print localDic[item]
            resultDic = {k:v for k, v in localDic.iteritems() \
                         if v >= minSup}
            #Here we just print out 2-coauthors
            if len(resultDic) >= 1:
                print "%s\t%s" % (currentName, resultDic.items())

        except:
            print "%s\t%s" %("inner err", "sorry!")
            pass

if __name__ == "__main__":
    support = 80
    main(support)
