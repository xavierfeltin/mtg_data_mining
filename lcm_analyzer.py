# -*- coding: utf-8 -*-
import numpy as np
from collections import OrderedDict
from operator import itemgetter


class LCMAnalyzer:
    """
    Bibliography:
    - http://research.nii.ac.jp/~uno/code/lcm.html
    - Takeaki Uno, Masashi Kiyomi, Hiroki Arimura :
       * LCM ver.3: Collaboration of Array, Bitmap and Prefix Tree for Frequent Itemset Mining, Open Source Data Mining Workshop on Frequent Pattern Mining Implementations 2005, Aug/2005
       * LCM ver.2: Efficient Mining Algorithms for Frequent/Closed/Maximal Itemsets," in Proceedings of IEEE ICDM'04 Workshop FIMI'04, 1/Nov/2004,
       http://sunsite.informatik.rwth-aachen.de/Publications/CEUR-WS//Vol-126/
    - Takeaki Uno and Tatsuya Asai, Hiroaki Arimura and Yuzo Uchida:
        * "LCM: An Efficient Algorithm for Enumerating Frequent Closed Item Sets," Workshop on Frequent Itemset Mining Implementations (FIMI'03),
        http://sunsite.informatik.rwth-aachen.de/Publications/CEUR-WS//Vol-90/
    """

    ALL_FREQUENT_ITEMSETS = 0
    MAXIMAL_ITEMSETS = 1
    CLOSED_ITEMSETS = 2

    def __init__(self, min_support = 0.2, c = 12):
        """
        :param min_support: the minimal frequence of apparition of an itemset to be considered frequent (in percentage)
        :param c: constant defining the constant suffix and prefix in transactions
        """
        self.support = min_support
        self.c = c

        self.nb_transactions = 0
        self.database_size = 0
        self.max_len_transaction = 0
        self.items = {}
        self.sorted_items = None
        self.mapping_items = {}

        self.transactions = None
        self.weights = None #weights of the transactions

        self.complete_prefix_tree = None

        self.occurences = None
        self.bitmap = None
        self.prefix_tree = None
        self.conditional_database = None
        self.database = None

    def load_data(self, database):
        """
        Initialize the parser with the transactions present in the database
        :param database: transaction database
        :return: None
        """

        #Scan the database to initialize the frequence of all items used in the transactions
        self.nb_transactions = len(database)
        for transaction in database:
            for item in transaction:
                if item in self.items:
                    self.items[item] += 1
                else:
                    self.items[item] = 1

                self.database_size += 1

            if len(transaction) > self.max_len_transaction:
                self.max_len_transaction = len(transaction)

        #Sort the items by increasing frequencies and renumerate the items (most frequent items = biggest number)
        #Skip the items with a frequency lower than the support
        self.sorted_items = OrderedDict(sorted(self.items.items(), key = (itemgetter(1), itemgetter(0)), reverse = (False, False)))
        for index, item, freq in enumerate(self.sorted_items.items()):
            if freq >= self.support:
                self.mapping_items[item] = index+1

        #By default all transactions have a weight of one
        self.weights = np.ndarray.ones(self.nb_transactions)

        #Initialize the bitmap representation of the database
        

    def mining(self, mode = CLOSED_ITEMSETS):
        """
        Mine the database to extract the frequent items
        :param mode: define the type of frequents itemsets to be extracted
        :return: list of frequent itemsets
        """
        pass