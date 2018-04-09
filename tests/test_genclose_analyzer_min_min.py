import unittest
from genclose_analyzer import GenCloseAnalyzer as GCA
from genclose_analyzer import RuleAssociationMinMin as RAMM
from genclose_analyzer import Rule

class TestGenCloseAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Validate the developments with the indications published here:
        https://pdfs.semanticscholar.org/56a4/ec156b26225b5922182bacc4c5b26fd5a555.pdf
        """

        self.db = []
        self.db.append(['a','c','t','w'])
        self.db.append(['c','d','w'])
        self.db.append(['a','c','t','w'])
        self.db.append(['a','c','d','w'])
        self.db.append(['a','c','d','t','w'])
        self.db.append(['c','d','t'])

    def test_minimals(self):
        minimals = RAMM.get_minimals(set('AT'),[set('ADT'), set('TDW')])
        self.assertListEqual(minimals, [set('D')])
        minimals = RAMM.get_minimals(set('TW'), [set('ADT'), set('TDW')])
        self.assertListEqual(minimals, [set('D')])

    def test_mine_basic_rules_LS_1(self):
        analyzer = GCA(self.db, 0.0)
        analyzer.clean_database()
        analyzer.mine()

        L = set(['a','c','t','w'])
        S = set(['a','c','d','t','w'])

        L_node = analyzer.search_node_with_closure(L)
        S_node = analyzer.search_node_with_closure(S)

        rule_miner = RAMM(analyzer.lcg_into_list())
        B_LS = rule_miner.mine_LS(L_node, S_node, 0.0, 1.0, 0.0, 1.0)
        rules = []
        rules.append(Rule(set(['a','t']), set(['d'])))
        rules.append(Rule(set(['t','w']), set(['d'])))
        self.assertIn(B_LS, rules)
        self.assertTrue(True)

    def test_mine_basic_rules_LS_2(self):
        analyzer = GCA(self.db, 0.0)
        analyzer.clean_database()
        analyzer.mine()

        L = set(['c','d'])
        S = set(['a','c','d','t','w'])

        L_node = analyzer.search_node_with_closure(L)
        S_node = analyzer.search_node_with_closure(S)

        rule_miner = RAMM(analyzer.lcg_into_list())
        B_LS = rule_miner.mine_LS(L_node, S_node, 0.0, 1.0, 0.0, 1.0)
        rules = []
        rules.append(Rule(set(['d']), set(['a','t'])))
        rules.append(Rule(set(['d']), set(['t','w'])))
        self.assertIn(B_LS, rules)
        self.assertTrue(True)

