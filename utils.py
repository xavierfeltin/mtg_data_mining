# -*- coding: utf-8 -*-

class TreeNode:
    "Class to manage FPGrowth tree nodes"
    def __init__(self, nameValue, numOccur, parentNode):
        self.name = nameValue
        self.count = numOccur
        self.nodeLink = None #link to similar items
        self.parent = parentNode
        self.children = {}

    def inc(self, numOccur):
        self.count += numOccur

    def display(self, ind=1):
        print (' '*ind, self.name, ' ', self.count)
        for child in self.children.values():
            child.display(ind+1)