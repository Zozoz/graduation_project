#!/usr/bin/env python
# encoding: utf-8


import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class treeNode:
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def disp(self, ind=1):
        print ' '*ind, self.name, ' ', self.count
        for child in self.children.values():
            child.disp(ind+1)

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


def getData(filename):
    dataItemSet = []
    with open(filename, 'r') as f:
        for line in f:
            line = line.strip('\n').split(' ')[1:]
            dataItemSet.append(line)
    # print dataItemSet
    return dataItemSet



def loadSimpleData():
    simpDat = [['f', 'a', 'c', 'd', 'g', 'i', 'm', 'p'],
            ['a', 'b', 'c', 'f', 'l', 'm', 'o'],
            ['b', 'f', 'h','j', 'o'],
            ['b', 'c', 'k', 's', 'p'],
            ['a', 'f', 'c', 'e', 'l', 'p', 'm', 'n']
            ]
    return simpDat


def createInitSet(dataSet):
    retDict = {}
    for trans in dataSet:
        retDict[frozenset(trans)] = 1
    return retDict, len(dataSet)


def createTree(dataSet, minSup=1):
    headerTable = {}
    for trans in dataSet:
        for item in trans:
            headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

    for k in headerTable.keys():
        if headerTable[k] < minSup:
            del(headerTable[k])

    freqItemSet = set(headerTable.keys())
    # print headerTable
    if len(freqItemSet) == 0:
        return None, None, freqItemSet

    for k in headerTable:
        headerTable[k] = [headerTable[k], None]
    retTree = treeNode('Null', 1, None)
    for tranSet, count in dataSet.items():
        localD = {}
        for item in tranSet:
            if item in freqItemSet:
                localD[item] = headerTable[item][0]
        if len(localD) > 0:
            orderedItems = [v[0] for v in sorted(localD.items(),
                key=lambda p: p[1], reverse=True)]
            updateTree(orderedItems, retTree, headerTable, count)

    return retTree, headerTable, freqItemSet


def updateTree(items, inTree, headerTable, count):
    if items[0] in inTree.children:
        inTree.children[items[0]].inc(count)
    else:
        inTree.children[items[0]] = treeNode(items[0], count, inTree)
        if headerTable[items[0]][1] == None:
            headerTable[items[0]][1] = inTree.children[items[0]]
        else:
            updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

    if len(items) > 1:
        updateTree(items[1:], inTree.children[items[0]], headerTable, count)


def updateHeader(nodeToTest, targetNode):
    while(nodeToTest.nodeLink != None):
        nodeToTest = nodeToTest.nodeLink
    nodeToTest.nodeLink = targetNode


def ascendTree(leafNode, prefixPath):
    if leafNode.parent != None:
        prefixPath.append(leafNode.name)
        ascendTree(leafNode.parent, prefixPath)


def findPrefixPath(baseSet, treeNode):
    condPats = {}
    while treeNode != None:
        prefixPath = []
        ascendTree(treeNode, prefixPath)
        if len(prefixPath) > 1:
            condPats[frozenset(prefixPath[1:])] = treeNode.count
        treeNode = treeNode.nodeLink
    return condPats


def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
    bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
    for basePat in bigL:
        newFreqSet = preFix.copy()
        newFreqSet.add(basePat)
        freqItemList.append(list(newFreqSet))
        condPattBases = findPrefixPath(basePat, headerTable[basePat][1])
        myCondTree, myHead, f = createTree(condPattBases, minSup)
        if myHead != None:
            # print 'conditional tree for: ', newFreqSet
            # myCondTree.disp(1)
            mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)


if __name__ == '__main__':
    # simpDat = loadSimpleData()
    filename = sys.argv[1]
    simpDat = getData(filename)
    initSet, sum = createInitSet(simpDat)
    minSup = sum * 0.6
    print 'sum = ', sum
    myFpTree, myHeaderTable, freqItemSet = createTree(initSet, minSup)
    # myFpTree.disp()
    # # return myFpTree, myHeaderTable, freqItemSet
    freqItem = []
    mineTree(myFpTree, myHeaderTable, minSup, set([]), freqItem)
    print '---------------------freqItem----------------------'
    freqItem.sort(key=lambda x: len(x))
    for item in freqItem:
        if len(item) > 1:
            print item



