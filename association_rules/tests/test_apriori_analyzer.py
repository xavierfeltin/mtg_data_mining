# coding=utf8
import unittest
from apriori_analyzer import APrioriAnalyzer

class TestAPrioriAnalyzer(unittest.TestCase):
    def setUp(self):
        "Load the sample dataset."
        self.dataset = [[1, 3, 4], [2, 3, 5], [1, 2, 3, 5], [2, 5]]

    def test_c1(self):
        analyzer = APrioriAnalyzer(self.dataset)
        c1 = analyzer.createC1(analyzer.dataset)
        self.assertTrue(len(list(c1)), 5)

    def test_scanD(self):
        analyzer = APrioriAnalyzer(self.dataset)
        c1 = analyzer.createC1(analyzer.dataset)
        l1, support_data = analyzer.scanD(analyzer.data_into_set, c1, 0.5)
        self.assertEqual(len(list(l1)), 4)
        self.assertIn(frozenset({1}), l1)
        self.assertIn(frozenset({2}), l1)
        self.assertIn(frozenset({3}), l1)
        self.assertIn(frozenset({5}), l1)

        self.assertEqual(support_data[frozenset({1})],0.5)
        self.assertEqual(support_data[frozenset({2})], 0.75)
        self.assertEqual(support_data[frozenset({3})], 0.75)
        self.assertEqual(support_data[frozenset({4})], 0.25)
        self.assertEqual(support_data[frozenset({5})], 0.75)

    def test_aprioriGen(self):
        analyzer = APrioriAnalyzer(self.dataset)
        c1 = analyzer.createC1(analyzer.dataset)
        l1, support_data = analyzer.scanD(analyzer.data_into_set, c1, 0.5)
        gen = analyzer.aprioriGen(l1, 2)
        self.assertEqual(len(gen), 6)
        self.assertIn(frozenset({1,3}), gen)
        self.assertIn(frozenset({1, 2}), gen)
        self.assertIn(frozenset({1, 5}), gen)
        self.assertIn(frozenset({2, 3}), gen)
        self.assertIn(frozenset({3, 5}), gen)
        self.assertIn(frozenset({2, 5}), gen)

    def test_apriori(self):
        analyzer = APrioriAnalyzer(self.dataset)
        L, support_data = analyzer.apriori(self.dataset, minsupport=0.5)
        result = [item for sublist in L for item in sublist]

        self.assertEqual(len(result), 9)
        self.assertIn(frozenset({1}), result)
        self.assertIn(frozenset({3}), result)
        self.assertIn(frozenset({2}), result)
        self.assertIn(frozenset({5}), result)
        self.assertIn(frozenset({1, 3}), result)
        self.assertIn(frozenset({2, 3}), result)
        self.assertIn(frozenset({3, 5}), result)
        self.assertIn(frozenset({2, 5}), result)
        self.assertIn(frozenset({2, 3, 5}), result)

        self.assertEqual(support_data[frozenset({1})],0.5)
        self.assertEqual(support_data[frozenset({2})], 0.75)
        self.assertEqual(support_data[frozenset({3})], 0.75)
        self.assertEqual(support_data[frozenset({4})], 0.25)
        self.assertEqual(support_data[frozenset({5})], 0.75)
        self.assertEqual(support_data[frozenset({1,2})], 0.25)
        self.assertEqual(support_data[frozenset({1,3})], 0.5)
        self.assertEqual(support_data[frozenset({1,5})], 0.25)
        self.assertEqual(support_data[frozenset({2,3,5})], 0.5)
        self.assertEqual(support_data[frozenset({2,3})], 0.5)
        self.assertEqual(support_data[frozenset({2,5})], 0.75)
        self.assertEqual(support_data[frozenset({3,5})], 0.5)

    def test_generate_rules(self):
        analyzer = APrioriAnalyzer(self.dataset)
        L, support_data = analyzer.apriori(self.dataset, minsupport=0.5)
        rules = analyzer.generateRules(L, support_data, min_confidence=0.5)
        self.assertEqual(len(rules), 11)