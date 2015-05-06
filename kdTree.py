#!/usr/bin/env python
# encoding: utf-8


import operator
from collections import deque


COMPARE_CHILD = {
        0: (operator.le, operator.sub),
        1: (operator.ge, operator.add)
        }

class treeNode:
    def __init__(self, data=None, parentNode=None, dimension=0, axis=0, lchild=None, rchild=None):
        self.axis = axis
        self.dataList = data
        self.parent = parentNode
        self.dimension = dimension
        self.lchild = lchild
        self.rchild = rchild


    def distance(self, node):
        """
        return distance between current node and given node(like [3, 5,2])
        """
        return sum([pow(self.dataList[i] - node[i], 2) for i in range(len(self.dataList))])


    def children(self):
        if self.lchild and self.lchild.dataList is not None:
            yield self.lchild, 0
        if self.rchild and self.rchild.dataList is not None:
            yield self.rchild, 1


    def height(self):
        min_height = int(bool(self))
        return max([min_height] + [c.height() + 1 for c, p in self.children()])


    def search_kn(self, node, k, dist=None):
        prev = None
        current = self

        get_dist = lambda n: n.distance(node)

        parents = {current: None}

        while current.dataList:
            axis = current.axis
            if node[axis] < current.dataList[axis]:
                parents[current.lchild] = current
                prev = current
                current = current.lchild
            else:
                parents[current.rchild] = current
                prev = current
                current = current.rchild
            if not current:
                break

        if not prev:
            return []

        examined = set()
        results = {}

        current = prev
        while current:
            current._search_node(node, k, results, examined, get_dist)
            current = parents[current]

        return sorted(results.items(), key=lambda kv: kv[1]) # sort by value


    def _search_node(self, node, k, results, examined, get_dist):
        examined.add(self)

        if not results:
            bestNode = None
            bestDist = float('inf')
        else:
            bestNode, bestDist = sorted(results.items(), key=lambda kv: kv[1], reverse=True)[0]

        nodesChanged = False

        nodeDist = get_dist(self)
        if nodeDist < bestDist:
            if len(results) == k and bestNode:
                results.pop(bestNode)
            results[self] = nodeDist
            nodesChanged = True
        elif nodeDist == bestDist:
            results[self] = nodeDist
            nodesChanged = True
        elif len(results) < k:
            results[self] = nodeDist
            nodesChanged = True

        if nodesChanged:
            bestNode, bestDist = next(iter(
                sorted(results.items(), key=lambda kv: kv[1], reverse=True)
                ))

        for child, pos in self.children():
            if child in examined:
                continue
            examined.add(child)
            compare, combine = COMPARE_CHILD[pos]

            nodePoint = self.dataList[self.axis]
            pointPlusDist = combine(node[self.axis], bestDist)
            lineIntersects = compare(pointPlusDist, nodePoint)
            if lineIntersects:
                child._search_node(node, k, results, examined, get_dist)


def getData():
    return [[2, 3], [5, 4], [9, 6], [4, 7], [8, 1], [7, 2]]


def create(dataList=None, parentNode=None, dimension=None, axis=0):
    if not dataList:
        return treeNode(dataList, parentNode, dimension, axis)
    axis = axis % dimension
    dataList.sort(key=lambda node: node[axis])
    midpos = len(dataList) // 2
    midNode = dataList[midpos]
    retNode = treeNode(midNode, parentNode, dimension, axis)
    retNode.lchild = create(dataList[:midpos], retNode, dimension, axis + 1)
    retNode.rchild = create(dataList[midpos + 1:], retNode, dimension, axis + 1)
    if not retNode.lchild.dataList:
        retNode.lchild = None
    if not retNode.rchild.dataList:
        retNode.rchild = None
    return retNode

def query(retTree, node):
    pass


def level_order(tree, include_all=False):
    q = deque()
    q.append(tree)
    while q:
        node = q.popleft()
        yield node
        if node.lchild:
            q.append(node.lchild)
        if node.rchild:
            q.append(node.rchild)


def visualize(tree, max_level=100, node_width=10, left_padding=5):
    height = min(max_level, tree.height() - 1)
    max_width = pow(2, height)
    per_level = 1
    in_level = 0
    level = 0
    for node in level_order(tree, include_all=False):
        if in_level == 0:
            print ''
            print ''
            print ' '*left_padding,

        width = int(max_width*node_width/per_level)
        node_str = (str(node.dataList) if node else '').center(width)
        print node_str,

        in_level += 1
        if in_level == per_level:
            in_level = 0
            per_level *= 2
            level += 1

        if level > height:
            break

    print ''
    print ''


if __name__ == '__main__':
    dataSet = getData()
    retTree = create(dataSet, None, 2, 0)
    visualize(retTree)
    results = retTree.search_kn([4, 2], 3)
    print '-'*80
    for k, v in results:
        print k.dataList, ' distance = ', v


