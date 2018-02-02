import csv

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

class FPGrowthAnalyzer:
    """
    Perform the FPGrowth analysis on the data and determine the most frequent items
    Bibliography :
    - http://blog.khaledtannir.net/2012/07/lalgorithme-fp-growth-les-bases-13/
    - https://www.singularities.com/blog/2015/08/apriori-vs-fpgrowth-for-frequent-item-set-mining
    - Machine Learning In Action, Peter Harrington, Manning, 2012
    - http://www.borgelt.net/doc/fpgrowth/fpgrowth.html
    """

    @staticmethod
    def createInitSet(dataSet):
        retDict = {}
        for trans in dataSet:
            retDict[frozenset(trans)] = 1
        return retDict

    @staticmethod
    def createTree(dataSet, minSup=1):
        "Create a FP-Tree and its associate header table from the dataset in argument"
        #Build the Header table
        headerTable = {}
        for trans in dataSet:
            for item in trans:
                headerTable[item] = headerTable.get(item, 0) + dataSet[trans]

        keys = list(headerTable.keys())
        for k in keys:
            if headerTable[k] < minSup:
                headerTable.pop(k, None) #Deleting items not meeting the required support

        #freqItemSet = set(headerTable.keys())
        #XF: detected non deterministic behavior in building the tree for a same dataset
        #by using the code from Machine Learning In Action, Peter Harrington, Manning, 2012
        #Indication from http://blog.khaledtannir.net/2012/07/lalgorithme-fp-growth-construction-du-fp-tree-13/
        #Sort header table by decreasing order of frequency ()
        freqItemSet = [v[0] for v in sorted(headerTable.items(), key=lambda p: (-p[1], p[0]), reverse=False)]

        if len(freqItemSet) == 0: return None, None
        for k in headerTable:
            headerTable[k] = [headerTable[k], None]

        #Sort items in a transaction by their frequency
        #Build the tree based on each transaction by integrating for each transaction the most frequent items first
        #Tree root is set to null as a stop point
        retTree = TreeNode('Null Set', 1, None)
        for tranSet, count in dataSet.items():
            localD = {}
            for item in tranSet:
                if item in freqItemSet:
                    localD[item] = headerTable[item][0]

            if len(localD) > 0:
                orderedItems = [v[0] for v in sorted(localD.items(), key=lambda p: (-p[1],p[0]), reverse=False)] #most frequent items first
                FPGrowthAnalyzer.updateTree(orderedItems, retTree, headerTable, count)

        return retTree, headerTable

    @staticmethod
    def updateTree(items, inTree, headerTable, count):
        "Update the tree with the ordered items of a transaction"
        if items[0] in inTree.children:
            #If the item is in the current branch increment the existing node
            inTree.children[items[0]].inc(count)
        else:
            #Fork the branch to create a new path
            inTree.children[items[0]] = TreeNode(items[0], count, inTree)

            #Update the header table with the new tree node information
            if headerTable[items[0]][1] == None:
                #If the first node for this item, attach a link from the header table to this node
                headerTable[items[0]][1] = inTree.children[items[0]]
            else:
                # If node already exist, attach the new node to the last node referenced for this item
                FPGrowthAnalyzer.updateHeader(headerTable[items[0]][1], inTree.children[items[0]])

        # Process the remaining items
        if len(items) > 1:
            FPGrowthAnalyzer.updateTree(items[1::], inTree.children[items[0]], headerTable, count)

    @staticmethod
    def updateHeader(nodeToTest, targetNode):
        "Add the targetNode at the end of the list of nodes starting with nodeToTest"
        while (nodeToTest.nodeLink != None):
            nodeToTest = nodeToTest.nodeLink
        nodeToTest.nodeLink = targetNode

    @staticmethod
    def ascendTree(leafNode, prefixPath):
        "Build the path from the leaf node until the tree root"
        if leafNode.parent != None:
            prefixPath.append(leafNode.name)
            FPGrowthAnalyzer.ascendTree(leafNode.parent, prefixPath)

    @staticmethod
    def findPrefixPath(basePat, treeNode):
        """
        Search all the conditional paths from each item in the list starting with treeNode"
        Each path is pondered by the frequency of the starting item
        """
        condPats = {}

        while treeNode != None:
            prefixPath = []
            FPGrowthAnalyzer.ascendTree(treeNode, prefixPath)
            if len(prefixPath) > 1:
                condPats[frozenset(prefixPath[1:])] = treeNode.count
            treeNode = treeNode.nodeLink
        return condPats

    @staticmethod
    def mineTree(inTree, headerTable, minSup, preFix, freqItemList):
        "Mine the tree by building FP-Trees for conditional paths until no more complex paths fit the minSup requirement"

        #Start the mining from the bottom of the header table (less frequent items first)
        #bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: p[1])]
        bigL = [v[0] for v in sorted(headerTable.items(), key=lambda p: (p[1][0], p[0]), reverse=False)]

        #Build a new tree (and associated header table) for each path and new child paths until no more fit the minSup
        for basePat in bigL:
            newFreqSet = preFix.copy()
            newFreqSet.add(basePat)
            freqItemList.append(newFreqSet)
            condPattBases = FPGrowthAnalyzer.findPrefixPath(basePat, headerTable[basePat][1])
            myCondTree, myHead = FPGrowthAnalyzer.createTree(condPattBases, minSup)
            if myHead != None:
                FPGrowthAnalyzer.mineTree(myCondTree, myHead, minSup, newFreqSet, freqItemList)

    @staticmethod
    def export_frequent_items(filename, freqItemList):
        "Save the items into a csv file"

        with open('./output/' + filename + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(['Frequent set of cards'])
            for itemList in freqItemList:
                line = []
                for item in itemList:
                    line.append(item)
                writer.writerow(line)