# -*- coding: utf-8 -*-
import csv
from pathlib import Path
from tqdm import tqdm

class APrioriAnalyzer:
    """
    Perform the APriori analysis on the data
    and determine the most frequent items and the associations rules between the different items
    Bibliography :
    - http://aimotion.blogspot.fr/2013/01/machine-learning-and-data-mining.html
    - https://en.wikipedia.org/wiki/Lift_(data_mining)
    - https://www.kdnuggets.com/2016/04/association-rules-apriori-algorithm-tutorial.html
    - http://data-mining.philippe-fournier-viger.com/how-to-auto-adjust-the-minimum-support-threshold-according-to-the-data-size/
    - Machine Learning In Action, Peter Harrington, Manning, 2012
    """

    def __init__(self, dataset):
        self.dataset = dataset
        self.data_into_set = [set(x) for x in self.dataset]

    def create_cache_count(self, dataset):
        "Generae a cache for the first level of candidates"
        candidates = self.createC1(dataset)
        sscnt = self.subcount(dataset, candidates)

        with open('./cache/cache_count.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            for frozen_card, count in sscnt.items():
                card = next(iter(frozen_card))
                line = [card, count]
                writer.writerow(line)
        return sscnt

    def export_rules(self, filename, rules):
        "Save the rules into a csv file"

        with open('./output/'+filename+'.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(['Confidence'])
            for rule in rules:
                line = []
                line.append(rule[2])
                for card in rule[0]:
                    line.append(card)
                line.append('---->')
                for card in rule[1]:
                    line.append(card)
                writer.writerow(line)

    @staticmethod
    def load_cache_count():
        "Load the cache from a CSV file"

        my_file = Path('./cache/cache_count.csv')
        if my_file.exists():
            cache = {}
            with open('./cache/cache_count.csv', newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                for row in reader:
                    card = frozenset({row[0]})
                    cache[card] = int(row[1])
            return cache
        else:
            return None

    def createC1(self, dataset):
        "Create a list of candidate item sets of size one."
        c1 = []
        for transaction in dataset:
            for item in transaction:
                if not [item] in c1:
                    c1.append([item])
        c1.sort()
        # frozenset because it will be a ket of a dictionary.
        return map(frozenset, c1)

    def subcount(self, dataset, candidates):
        "Counnt the number of occurances of each candidate in the dataset"
        sscnt = {}
        list_candidates = list(candidates)[:]
        for tid in dataset:
            for can in list_candidates:
                if can.issubset(tid):
                    sscnt.setdefault(can, 0)
                    sscnt[can] += 1
        return sscnt

    def scanD(self, dataset, candidates, min_support, cache_count = None):
        "Returns all candidates that meets a minimum support level"
        if cache_count is None:
            sscnt = self.subcount(dataset,candidates)
        else:
            sscnt = cache_count

        num_items = float(len(dataset))
        retlist = []
        support_data = {}
        print('Select candidates with support > ' + str(min_support))
        for key in tqdm(sscnt):
            support = sscnt[key] / num_items
            if support >= min_support:
                retlist.insert(0, key)
            support_data[key] = support
        return retlist, support_data

    def aprioriGen(self, freq_sets, k):
        "Generate the joint transactions from candidate sets"
        retList = []
        lenLk = len(freq_sets)

        print('generate C' + str(k))
        for i in tqdm(range(lenLk)):
            for j in range(i + 1, lenLk):
                L1 = list(freq_sets[i])[:k - 2]  #k-2 to check only the beginning of the set
                L2 = list(freq_sets[j])[:k - 2]
                L1.sort()
                L2.sort()
                if L1 == L2:
                    retList.append(freq_sets[i] | freq_sets[j])
        return retList

    def apriori(self, dataset, minsupport=0.5, cache_count = None):
        "Generate a list of candidate item sets"
        if cache_count is None: C1 = self.createC1(dataset)
        else: C1 = None #Already computed inside the cache

        D = self.data_into_set
        L1, support_data = self.scanD(D, C1, minsupport, cache_count)
        L = [L1]
        k = 2
        while (len(L[k - 2]) > 0):
            Ck = self.aprioriGen(L[k - 2], k)
            Lk, supK = self.scanD(D, Ck, minsupport)
            support_data.update(supK)
            L.append(Lk)
            k += 1

        return L, support_data

    def generateRules(self, L, support_data, min_confidence=0.7):
        """Create the association rules
        L: list of frequent item sets
        support_data: support data for those itemsets
        min_confidence: minimum confidence threshold
        """
        rules = []
        print('generate rules')
        for i in tqdm(range(1, len(L))):
            for freqSet in L[i]:
                H1 = [frozenset([item]) for item in freqSet]
                print ("freqSet", freqSet, 'H1', H1)
                if (i > 1):
                    self.rules_from_conseq(freqSet, H1, support_data, rules, min_confidence)
                else:
                    self.calc_confidence(freqSet, H1, support_data, rules, min_confidence)

        return rules

    def calc_confidence(self, freqSet, H, support_data, rules, min_confidence=0.7, min_lift = 1.1):
        "Evaluate the rule generated through the confidence and the lift"
        pruned_H = []
        for conseq in H:
            conf = support_data[freqSet] / support_data[freqSet - conseq]
            lift = conf/support_data[conseq]
            if conf >= min_confidence and lift >= min_lift: #Reject unassociated items (lift of 1)
                print(freqSet - conseq, '--->', conseq, 'conf:', conf, 'lift:', lift)
                rules.append((freqSet - conseq, conseq, conf))
                pruned_H.append(conseq)
        return pruned_H

    def rules_from_conseq(self, freqSet, H, support_data, rules, min_confidence=0.7):
        "Generate a set of candidate rules"
        m = len(H[0])
        if (len(freqSet) > (m + 1)):
            Hmp1 = self.aprioriGen(H, m + 1)
            Hmp1 = self.calc_confidence(freqSet, Hmp1, support_data, rules, min_confidence)
            if len(Hmp1) > 1:
                self.rules_from_conseq(freqSet, Hmp1, support_data, rules, min_confidence)