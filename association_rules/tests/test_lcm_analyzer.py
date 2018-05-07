# coding=utf8
import unittest
import numpy as np
from lcm_analyzer import LCMAnalyzer
from utils import TreeNode

class TestAPrioriAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Load the sample dataset.

        From http://research.nii.ac.jp/~uno/code/lcm.html#References
        With a support of 3:
            All frequent itemsets: {}, {1}, {2}, {7}, {9}, {1,7}, {1,9}, {2,7}, {2,9}, {7,9}, and {2,7,9}
            Maximal itemsets:  {1,7}, {1,9}, and {2,7,9}
            Closed itemsets:  {}, {2}, {2,5}, {7,9}, {1,7,9}, {2,7,9}, {1,2,7,9}, {2,3,4,5}, {1,2,7,8,9}, and {1,2,5,6,7,9}
        """
        self.dataset = [[1,2,5,6,7], [2,3,4,5], [1,2,7,8,9], [1,7,9], [2,7,9], [2]]
        self.transactions_to_sort = [[7,6,5,2,1], [5,4,3,2], [9,8,7,2,1], [9,7,1], [9,2,7,1], [9,2,7], [2]]
        self.transactions_to_merge = [[9,8,7,2,1], [9, 7, 1], [9, 7, 1], [9, 2, 7], [9, 2, 7, 1],
                                      [7, 6, 5, 2, 1], [5, 4, 3, 2], [2], [2]]

    def test_load_database(self):
        lcm = LCMAnalyzer()
        lcm.load_data(self.dataset)

        self.assertEqual(len(lcm.transactions), 6)
        self.assertEqual(lcm.weights.sum(),6)
        for transaction in lcm.transactions:
            self.assertEqual(len(transaction), 1) #All fits in bitmap format

        #Check the conversion into bit maps for c most frequent items
        self.assertEqual("{0:b}".format(lcm.transactions[0][0]), '111101000')
        self.assertEqual("{0:b}".format(lcm.transactions[1][0]), '111000000')

    def test_radix_sort(self):
        sorted = LCMAnalyzer.radix_sort(self.transactions_to_sort)
        self.assertListEqual(sorted[0], [9,8,7,2,1])
        self.assertListEqual(sorted[1], [9, 7, 1])
        self.assertListEqual(sorted[2], [9, 2, 7])
        self.assertListEqual(sorted[3], [9, 2, 7, 1])
        self.assertListEqual(sorted[4], [7, 6, 5, 2, 1])
        self.assertListEqual(sorted[5], [5, 4, 3, 2])
        self.assertListEqual(sorted[6], [2])

    def test_merge_transactions(self):
        merged_transactions, merged_weights = LCMAnalyzer.merge_transactions(self.transactions_to_merge,np.ones(len(self.transactions_to_merge)))

        self.assertListEqual(merged_transactions[0], [9, 8, 7, 2, 1])
        self.assertListEqual(merged_transactions[1], [9, 7, 1])
        self.assertListEqual(merged_transactions[2], [9, 2, 7])
        self.assertListEqual(merged_transactions[3], [9, 2, 7, 1])
        self.assertListEqual(merged_transactions[4], [7, 6, 5, 2, 1])
        self.assertListEqual(merged_transactions[5], [5, 4, 3, 2])
        self.assertListEqual(merged_transactions[6], [2])
        self.assertListEqual(list(merged_weights), [1,2,1,1,1,1,2])

    def test_build_prefix_complete_tree(self):
        tree = TreeNode(0,0,None)
        LCMAnalyzer.build_complete_prefix_tree(tree, 4)
        self.assertEqual(tree.count_nodes(), 16)

    def test_build_conditional_database(self):

        weights = np.ones(len(self.transactions_to_merge), dtype=int)
        p_itemset = frozenset({7})
        p_tail = 7
        support = 0.2
        all_transactions_items, conditional_database, conditional_weights = LCMAnalyzer.build_conditional_database(self.transactions_to_merge, weights, p_itemset, p_tail, support)

        self.assertListEqual(all_transactions_items, [9]) #9 is common to all transactions in Tp
        self.assertEqual(len(conditional_database[0]), 0)  # transactions containing only 9
        self.assertEqual(conditional_database[1][0], 8)  # other transaction containing 8
        self.assertEqual(conditional_weights[0], 4) # 4 identical transactions with 9
        self.assertEqual(conditional_weights[1], 1)  # 1 transaction with 8
        self.assertNotIn([1,2,3,4,5,6,7], conditional_database[0])
        self.assertNotIn([1, 2, 3, 4, 5, 6, 7], conditional_database[0]) # items < p_tail are deleted
        self.assertNotIn([1, 2, 3, 4, 5, 6, 7], conditional_database[1]) # items < p_tail are deleted

    def test_occurence_delivery(self):
        weights = np.ones(len(self.transactions_to_merge), dtype=int)
        p_itemset = frozenset({2})
        p_tail = 2
        support = 0.2
        all_transactions_items, conditional_database, conditional_weights = LCMAnalyzer.build_conditional_database(self.transactions_to_merge, weights, p_itemset, p_tail, support)

        base, buckets = LCMAnalyzer.occurence_delivery(conditional_database)

        self.assertListEqual(base,[9,8,7,6,5,4,3])
        self.assertListEqual(buckets[0], [0,1])
        self.assertListEqual(buckets[1], [0])
        self.assertListEqual(buckets[2], [0,1,2])
        self.assertListEqual(buckets[3], [2])
        self.assertListEqual(buckets[4], [2,3])
        self.assertListEqual(buckets[5], [3])
        self.assertListEqual(buckets[6], [3])