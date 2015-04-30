#!/usr/bin/env python
# encoding: utf-8
import sys

def getdata(filename):
    dataDict = {}
    a = 0
    with open(filename, 'r') as f:
        for line in f:
            a += 1
            if a == 1:
                continue
            print a
            line = line.split(',')
            if not dataDict.has_key(line[0]):
                dataDict[line[0]] = set([line[1].strip('\n')])
            else:
                dataDict[line[0]].add(line[1].strip('\n'))
            if a > 10:
                break
    print 'sum of line:', a
    dataItemSet = []
    for k in dataDict:
        dataItemSet.append(dataDict[k])
    f = open('data.txt', 'w+')
    for item in dataItemSet:
        f.write(str(item) + '\n')


def splitdata(filename):
    a = 0
    dataItemSet = []
    with open(filename, 'r') as f:
        for line in f:
            a += 1
            line = line.split(',')
            line[-1] = line[-1].strip('\n')
            dataItemSet.append(line[1:])
            if a > 100:
                break
    print dataItemSet


def partition(filename):
    cnt = 0
    fp = open('small.data', 'w')
    with open(filename, 'r') as f:
        for line in f:
            fp.write(line)
            cnt += 1
            if cnt == 100:
                break

if __name__ == '__main__':
    filename = sys.argv[1]
    print filename
    # getdata(filename)
    # plitdata(filename)
    partition(filename)


