# coding=utf8
import unittest
from lcm_analyzer import LCMAnalyzer

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
        self.sorted_transactions_dataset = [[7,6,5,2,1], [5,4,3,2], [9,8,7,2,1], [9,7,1], [9,2,7,1], [9,2,7], [2]]

    def test_load_database(self):
        lcm = LCMAnalyzer()
        lcm.load_data(self.dataset)

        self.assertTrue(True)

    def test_radix_sort(self):
        sorted = LCMAnalyzer.radix_sort(self.sorted_transactions_dataset)
        self.assertListEqual(sorted[0], [9,8,7,2,1])
        self.assertListEqual(sorted[1], [9, 7, 1])
        self.assertListEqual(sorted[2], [9, 2, 7])
        self.assertListEqual(sorted[3], [9, 2, 7, 1])
        self.assertListEqual(sorted[4], [7, 6, 5, 2, 1])
        self.assertListEqual(sorted[5], [5, 4, 3, 2])
        self.assertListEqual(sorted[6], [2])
