# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#

class TreeNode:
    "Class to manage FPGrowth tree nodes"
    def __init__(self, nameValue, numOccur, parentNode):
        self.value = nameValue
        self.count = numOccur
        self.nodeLink = None #link to similar items
        self.parent = parentNode
        self.children = []

    def inc(self, numOccur):
        self.count += numOccur

    def add_child(self, child):
        self.children.append(child)

    def display(self, ind=1):
        print (' '*ind, self.value, ' ', self.count)
        for child in self.children:
            child.display(ind+1)

    def count_nodes(self, ind=1):
        if ind == 1:
            count = len(self.children) + 1 #add root
        else:
            count = len(self.children)

        for child in self.children:
            count += child.count_nodes(ind + 1)
        return count