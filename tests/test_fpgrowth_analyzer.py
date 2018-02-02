# coding=utf8
import unittest
from fpgrowth_analyzer import FPGrowthAnalyzer, TreeNode

class TestAPrioriAnalyzer(unittest.TestCase):
    def setUp(self):
        "Load the sample dataset."
        self.dataset = simpDat = [['r', 'z', 'h', 'j', 'p'],
                    ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
                    ['z'],
                    ['r', 'x', 'n', 'o', 's'],
                    ['y', 'r', 'x', 'z', 'q', 't', 'p'],
                    ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
        self.initSet = FPGrowthAnalyzer.createInitSet(self.dataset)

    def eval_count_node(self, start_node):
        count = 0
        node = start_node
        while node is not None:
            count += node.count
            node = node.nodeLink
        return count

    def test_create_tree(self):
        myFPtree, myHeaderTab = FPGrowthAnalyzer.createTree(self.initSet, 3)

        self.assertEqual(len(myHeaderTab), 6)
        self.assertEqual(myHeaderTab['r'][0], 3)
        self.assertIsInstance(myHeaderTab['r'][1], TreeNode)
        self.assertEqual(myHeaderTab['r'][0], self.eval_count_node(myHeaderTab['r'][1]))

        self.assertEqual(myHeaderTab['s'][0], 3)
        self.assertIsInstance(myHeaderTab['s'][1], TreeNode)
        self.assertEqual(myHeaderTab['s'][0], self.eval_count_node(myHeaderTab['s'][1]))

        self.assertEqual(myHeaderTab['t'][0], 3)
        self.assertIsInstance(myHeaderTab['t'][1], TreeNode)
        self.assertEqual(myHeaderTab['t'][0], self.eval_count_node(myHeaderTab['t'][1]))

        self.assertEqual(myHeaderTab['x'][0], 4)
        self.assertIsInstance(myHeaderTab['x'][1], TreeNode)
        self.assertEqual(myHeaderTab['x'][0], self.eval_count_node(myHeaderTab['x'][1]))

        self.assertEqual(myHeaderTab['y'][0], 3)
        self.assertIsInstance(myHeaderTab['y'][1], TreeNode)
        self.assertEqual(myHeaderTab['y'][0], self.eval_count_node(myHeaderTab['y'][1]))

        self.assertEqual(myHeaderTab['z'][0], 5)
        self.assertIsInstance(myHeaderTab['z'][1], TreeNode)
        self.assertEqual(myHeaderTab['z'][0], self.eval_count_node(myHeaderTab['z'][1]))

    def test_prefix_path(self):
        myFPtree, myHeaderTab = FPGrowthAnalyzer.createTree(self.initSet, 3)
        path = FPGrowthAnalyzer.findPrefixPath('x', myHeaderTab['x'][1])
        self.assertIn(frozenset('z'), path)
        self.assertEqual(path[frozenset('z')], 3)

        path = FPGrowthAnalyzer.findPrefixPath('r', myHeaderTab['r'][1])
        self.assertIn(frozenset('z'), path)
        self.assertEqual(path[frozenset('z')], 1)
        self.assertIn(frozenset('x'), path)
        self.assertEqual(path[frozenset('x')], 1)
        self.assertIn(frozenset(['x', 'z']), path)
        self.assertEqual(path[frozenset(['x', 'z'])], 1)

    def test_mine_tree(self):
        myFPtree, myHeaderTab = FPGrowthAnalyzer.createTree(self.initSet, 3)
        freqItems = []
        FPGrowthAnalyzer.mineTree(myFPtree, myHeaderTab, 3, set([]), freqItems)
        self.assertEqual(len(freqItems), 18)
