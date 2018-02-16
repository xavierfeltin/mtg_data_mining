# -*- coding: utf-8 -*-
import numpy as np
from collections import OrderedDict
from operator import itemgetter
from math import inf

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
    END_NUMBER = 65000 #In Magic The Gathering, there are 19 000 cards at the moment. Avoid to use Float with math.inf

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
        self.most_frequent_items = [] #c last items

        self.transactions = []
        self.weights = None #weights of the transactions

        self.complete_prefix_tree = None

        self.occurences = None
        self.bitmap = None
        self.prefix_tree = None
        self.conditional_database = None
        self.database = None

    @staticmethod
    def radix_sort(database):
        """
        Sort transactions in the database using radix sort
        example: [[7,6,5,2,1], [5,4,3,2], [9,8,7,2,1]]
        return: [[9,8,7,2,1], [7,6,5,2,1], [5,4,3,2]]
        :param database: list of transactions to sort
        :return: sorted database
        """
        def list_to_buckets(array_to_sort, database, iteration):
            """
            Place the transactions index into buckets matching the set of items at the considered level of the transactions
            The buckets are sorted by decreasing orders
            :param array_to_sort: list of transactions index to sort through the buckets
            :param database: list of all transactions
            :param iteration: considered level of transactions
            :return: list of sorted buckets containing the transactions index
            """

            # Build base for sorting
            base = []
            slice = []
            for index in array_to_sort:
                transaction = database[index]
                if len(transaction) > iteration:
                    if transaction[iteration] not in base:
                        base.append(transaction[iteration])
                    slice.append(transaction[iteration])
                else:
                    if LCMAnalyzer.END_NUMBER not in base:
                        base.append(LCMAnalyzer.END_NUMBER)
                    slice.append(LCMAnalyzer.END_NUMBER)
            base.sort(reverse=True)

            buckets = [[] for _ in base]
            for index, number in enumerate(slice):
                # Drop the into the correct bucket
                buckets[base.index(number)].append(array_to_sort[index])
            return buckets

        def sort_bucket(bucket, database, max_nb_items, iteration):
            """
            Recursively sort the buckets if there are more than one element
            :param bucket: bucket containing the transactions index to sort at the next level
            :param database: list of all transactions
            :param max_nb_items: max length of a transaction in the database
            :param iteration: considered level of transactions
            :return: sorted transactions index based on the items contained in each transactions
            """
            if len(bucket) > 1 and iteration < max_nb_items:
                new_buckets = list_to_buckets(bucket, database, iteration)
                sorted_array = []
                for new_bucket in new_buckets:
                    sorted_array.extend(sort_bucket(new_bucket, database, max_nb_items, iteration+1))
                return sorted_array
            return bucket

        index_array = list(range(0,len(database)))

        max_nb_items = 0
        for i, transaction in enumerate(database):
            if len(transaction) > max_nb_items: max_nb_items = len(transaction)

        # Sort the transactions by comparing each level of item
        it = 0
        buckets = list_to_buckets(index_array, database, it)
        sorted_indexes = []
        for bucket in buckets:
            sorted_indexes.extend(sort_bucket(bucket, database, max_nb_items, it+1))

        #Make a copy of the dataset matching the new order of the transactions
        sorted_database = np.ndarray(len(database), dtype=object)
        index = 0
        for sorted_index in sorted_indexes:
            sorted_database[index] = database[sorted_index].copy()
            index += 1

        return sorted_database

    @staticmethod
    def merge_transactions(transactions, weights):
        """
        Merge identic transactions into one transaction and increment the weight of the remaining transaction
        :param transactions: list of transactions to merge
        :param weights: list of weights to update
        :return: list of merged transactions, list of weights
        """

        merged_transactions = transactions[:]
        merged_weights = transactions[:]

        # Step 1: sort transactions using radix sort
        # Step 2: merge same transactions together and increase matching weights

        return merged_transactions, merged_weights


    def load_data(self, database):
        """
        Initialize the parser with the transactions present in the database
        :param database: transaction database
        :return: None
        """

        #Scan the database to initialize the frequence of all items used in the transactions
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

        #Cache the c most frequent items
        bit_position = self.c -1
        for i in range(self.c):
            it = reversed(self.sorted_items.items())
            self.most_frequent_items[item] = bit_position
            bit_position -= 1

        #Initialize the bitmap representation of the database
        #Reduce the database size by ignoring non frequent items and empty transactions
        self.transactions = np.ndarray(len(database), dtype=object)
        t_index = 0
        for transaction in database:
            list_items = np.ndarray.zeros(len(transaction)+1)
            list_items[0] = 0 #bitmap of c most frequent items in the current transaction
            index = 1
            for item in transaction:
                if item in self.most_frequent_items:
                    list_items[0][self.most_frequent_items[item]] = 1
                elif item in self.mapping_items:
                    list_items[index]
                    index += 1
            list_items.resize(index)

            # Keep non empty transactions : at least 1 item or bitmap > 0
            if index > 1 or list_items.sum() > 0:
                self.transactions[t_index] = list_items
                t_index += 1

        self.transactions.resize(t_index)
        self.nb_transactions = len(self.transactions)

        # By default all transactions have a weight of one
        self.weights = np.ndarray.ones(self.nb_transactions)

        #Reduce database size by merging same transactions together
        self.transactions, self.weights = LCMAnalyzer.merge_transactions(self.transactions, self.weights)


    def mining(self, mode = CLOSED_ITEMSETS):
        """
        Mine the database to extract the frequent items
        :param mode: define the type of frequents itemsets to be extracted
        :return: list of frequent itemsets
        """
        pass