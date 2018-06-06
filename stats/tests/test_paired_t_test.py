# -*- coding: utf-8 -*-
import unittest
from stats.paired_t_test import PairedTTest

class TestItemBasedDeshpande(unittest.TestCase):

    def setUp(self):
        #Serie of data before the event
        self.serie_1 = [18,21,16,22,19,24,17,21,23,18,14,16,16,19,18,20,12,22,15,17]

        # Serie of data after the event
        self.serie_2 = [22,25,17,24,16,29,20,23,19,20,15,15,18,26,18,24,18,25,19,16]

    def testResults(self):
        results = PairedTTest.get_results(self.serie_2, self.serie_1)
        self.assertEqual(round(results[0],4),3.2313)
        self.assertEqual(round(results[1],4), 0.0044)

    def testConfidenceInterval(self):
        confidence_interval = PairedTTest.get_confidence_interval(self.serie_2, self.serie_1, 0.95)
        self.assertEqual(round(confidence_interval[0],2), 2.05)
        self.assertEqual(round(confidence_interval[1],2), 0.72)
        self.assertEqual(round(confidence_interval[2],2), 3.38)