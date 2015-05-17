#!/usr/bin/env python
# encoding: utf-8


import redis
from optparse import OptionParser

def loadDataSet():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    # return [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]
    simpDat = [[1, 2, 3, 4],
            [2, 5, 4, 6],
            [2, 3, 4],
            [1, 2, 3, 5, 4, 6],
            [1, 3, 6],
            [2, 3, 6],
            [1, 3, 4],
            [1, 2, 3, 7, 4],
            [1, 2, 7, 4]
            ]
    return simpDat

def getdata(filename):
    dataDict = {}
    a = 0
    with open(filename, 'r') as f:
        for line in f:
            a += 1
            print a
            line = line.split(',')
            if not dataDict.has_key(line[0]):
                dataDict[line[0]] = set([line[1].strip('\n')])
            else:
                dataDict[line[0]].add(line[1].strip('\n'))
            if a > 100:
                break
    print 'sum of line:', a
    dataItemSet = []
    for k in dataDict:
        dataItemSet.append(dataDict[k])
    return dataItemSet

def getPoj(filename):
    cnt = 0
    dataItemSet = []
    with open(filename, 'r') as f:
        for line in f:
            cnt += 1
            print cnt
            line = line.split(' ')[1:]
            line[-1] = line[-1].strip('\n')
            line = set(line) - set(['1000', '1004', '1003', '1005', '1007', '1006', '1163', '1088', '1002', '1050'])
            line = list(line)
            dataItemSet.append(line)
    return dataItemSet


# return init frequent item, return type is list
def createC1(dataSet):
    C1 = []
    for tran in dataSet:
        for item in tran:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset, C1)

# return frequent item, return type is list.
def scanD(dataSet, Ck, minSupport):
    sumsup = {}
    for tran in dataSet:
        for item in Ck:
            if item.issubset(tran):
                if sumsup.has_key(item):
                    sumsup[item] += 1
                else:
                    sumsup[item] = 1

    numItems = float(len(dataSet))
    retList = []
    supportData = {}
    for item in sumsup:
        support = sumsup[item] / numItems
        if support >= minSupport:
            retList.insert(0, item)
        supportData[item] = support

    return retList, supportData

# merge two frequent set who have k-1 common front
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        for j in range(i+1, lenLk):
            L1 = list(Lk[i])[:k-2]
            L2 = list(Lk[j])[:k-2]
            L1.sort()
            L2.sort()
            if L1 == L2:
                retList.append(Lk[i] | Lk[j]) # merge Lk[i] and Lk[j]
    return retList


def apriori(dataSet, minSupport=0.5):
    C1 = createC1(dataSet)
    D = map(set, dataSet)
    L1, supportData = scanD(D, C1, minSupport)
    L = [L1]
    k = 2
    while(len(L[k-2]) > 0):
        Ck = aprioriGen(L[k-2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        supportData.update(supK)
        L.append(Lk)
        k += 1
    return L, supportData


def calcConf(freqSet, H, supportData, br1, minConf=0.7):
    prunedH = []
    for conseq in H:
        if freqSet - conseq == frozenset(['1207', '1002', '1005', '1000']):
            print 'yyyyyyy'
            print freqSet, conseq
        conf = supportData[freqSet] / supportData[freqSet-conseq]
        if conf >= minConf:
            # print freqSet-conseq, '-->', conseq, 'conf:', conf
            br1.append((freqSet-conseq, conseq, conf))
            prunedH.append(conseq)
    return prunedH


def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    if(len(freqSet) > (m+1)):
        Hmp1 = aprioriGen(H, m+1)
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        if(len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)


def generateRules(L, supportData, minConf=0.7):
    bigRuleList = []
    for i in range(1, len(L)):
        for freqSet in L[i]:
            H1 = [frozenset([item]) for item in freqSet]
            if(i > 1):
                rulesFromConseq(freqSet, H1, supportData, bigRuleList,\
                        minConf)
            else:
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList


from itertools import chain, combinations
def subsets(arr):
    """return non-empty subsets of arr"""
    return chain(*[combinations(arr, i+1) for i, a in enumerate(arr)])

def getRecommend(testdata, rules):
    data = map(frozenset, [x for x in subsets(testdata)])
    rec = set()
    for item in data:
        for rule in rules:
            if item.issubset(rule[0]):
                rec.add(rule[1])
    print '------------------recommend-----------------'
    ret = set()
    for item in rec:
        for it in item:
            ret.add(it)
    print ret
    return ret


def writeToRedis(dbname, freqItemList, rules):
    r = redis.Redis(host='localhost', port=6379, db=dbname)


if __name__ == '__main__':

    optparser = OptionParser()
    optparser.add_option('-f', '--inputFile',
                        dest='input',
                        default=None)
    optparser.add_option('-s', '--minSupport',
                        dest='minS',
                        default=0,
                        type='float')
    optparser.add_option('-c', '--minConfidence',
                        dest='minC',
                        default=0,
                        type='float')
    (options, args) = optparser.parse_args()
    filename = options.input
    minSupport = options.minS
    minConf = options.minC
    dataSet = getPoj(filename)

    freqSetList, supportData = apriori(dataSet, minSupport)

    ret = []
    print '------------------freqItem---------------------'
    for tran in freqSetList:
        for item in tran:
            ret.append((item, supportData[item]))
            print item
    ret.sort(key=lambda x: x[1], reverse=True)
    fp = open('freq_20000_25000.data', 'w')
    for item in ret:
        fp.write(str(item) + '\n')
    fp.close()

    rules = generateRules(freqSetList, supportData, minConf)

    fp = open('rules_20000_25000.data', 'w')
    print '------------------rules---------------------'
    for rule in rules:
        fp.write(str(rule) + '\n')
        print rule

    # getRecommend(['1000', '1002'], rules)

