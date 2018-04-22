import unittest
from association_rules.genclose_analyzer import GenCloseAnalyzer as GCA
from association_rules.genclose_analyzer import RuleAssociationMinMin as RAMM
from association_rules.genclose_analyzer import RuleAssociationMinMax as RAMMax
from association_rules.genclose_analyzer import Rule
from collections import deque

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

        self.db_RAR = []
        self.db_RAR.append([1,3,5,7])
        self.db_RAR.append([1,3,6,8])
        self.db_RAR.append([1,4,6,8])
        self.db_RAR.append([2,3,5,7])

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
        self.assertEqual(frozenset(B_LS[0].left), frozenset(rules[0].left))
        self.assertEqual(frozenset(B_LS[0].right), frozenset(rules[0].right))
        self.assertEqual(frozenset(B_LS[1].left), frozenset(rules[1].left))
        self.assertEqual(frozenset(B_LS[1].right), frozenset(rules[1].right))

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
        self.assertEqual(frozenset(B_LS[0].left), frozenset(rules[0].left))
        self.assertEqual(frozenset(B_LS[0].right), frozenset(rules[0].right))
        self.assertEqual(frozenset(B_LS[1].left), frozenset(rules[1].left))
        self.assertEqual(frozenset(B_LS[1].right), frozenset(rules[1].right))
        self.assertTrue(True)

    def test_mine_consequent_LS_1(self):
        analyzer = GCA(self.db, 0.0)
        analyzer.clean_database()
        analyzer.mine()

        L = set(['a', 'c', 't', 'w'])
        S = set(['a', 'c', 'd', 't', 'w'])
        L_node = analyzer.search_node_with_closure(L)
        S_node = analyzer.search_node_with_closure(S)

        rule_miner = RAMM(analyzer.lcg_into_list())
        C_LS = rule_miner.mine_cars_L_S(L_node, S_node, 0, 1, 0, 1, analyzer)
        self.assertTrue(True)

    def test_mine_consequent_LS_2(self):
        analyzer = GCA(self.db, 0.0)
        analyzer.clean_database()
        analyzer.mine()

        L = set(['c', 'd'])
        S = set(['a', 'c', 'd', 't', 'w'])
        L_node = analyzer.search_node_with_closure(L)
        S_node = analyzer.search_node_with_closure(S)

        rule_miner = RAMM(analyzer.lcg_into_list())
        C_LS = rule_miner.mine_cars_L_S(L_node, S_node, 0, 1, 0, 1, analyzer)
        self.assertTrue(True)

    def test_mine_RAR(self):
        analyzer = GCA(self.db_RAR, 0.0)
        analyzer.clean_database()
        analyzer.mine()

        L = set([3,5,7])
        S = set([1,3,5,7])
        L_node = analyzer.search_node_with_closure(L)
        S_node = analyzer.search_node_with_closure(S)

        rule_miner = RAMMax(analyzer.lcg_into_list())
        RAR = rule_miner.mine_RAR(L_node, S_node)
        self.assertTrue(True)

    def test_mine_CAR(self):
        analyzer = GCA(self.db_RAR, 0.25)
        analyzer.clean_database()
        analyzer.mine()

        L = set([3, 5, 7])
        S = set([1, 3, 5, 7])
        L_node = analyzer.search_node_with_closure(L)
        S_node = analyzer.search_node_with_closure(S)

        rule_miner = RAMMax(analyzer.lcg_into_list())
        RAR = rule_miner.mine_RAR(L_node, S_node,0.25,1.0, 0.0,1.0)
        CAR2 = rule_miner.mine_CAR2(L_node, S_node, RAR, analyzer)

        self.assertTrue(len(CAR2), 13)
        rules = []
        rules.append(Rule(set([5]), set([1,7])))
        rules.append(Rule(set([5]), set([1,3])))
        rules.append(Rule(set([5]), set([1])))
        rules.append(Rule(set([7]), set([1, 5])))
        rules.append(Rule(set([7]), set([1, 3])))
        rules.append(Rule(set([7]), set([1])))
        rules.append(Rule(set([3,5]), set([1,7])))
        rules.append(Rule(set([5,7]), set([1,3])))
        rules.append(Rule(set([3,5,7]), set([1])))
        rules.append(Rule(set([5,7]), set([1])))
        rules.append(Rule(set([3,5]), set([1])))
        rules.append(Rule(set([3,7]), set([1,5])))
        rules.append(Rule(set([3,7]), set([1])))
        for i in range(len(CAR2)):
            self.assertEqual(frozenset(CAR2[i].left), frozenset(rules[i].left))
            self.assertEqual(frozenset(CAR2[i].right), frozenset(rules[i].right))

    def test_all_rules(self):
        analyzer = GCA(self.db_RAR, 0.25)
        analyzer.clean_database()
        analyzer.mine()

        lattice = analyzer.lcg_into_lattice()
        rule_miner = RAMMax(analyzer.lcg_into_list())

        nb_rules = 0
        nb_basic_rules = 0
        for node in lattice.values():
            S = node.fci
            print('S: ' + str(S.closure))

            to_extract = deque()
            to_extract.append(node)
            to_extract.extend(node.children)
            visited = deque()
            while len(to_extract) > 0:
                current = to_extract.popleft()
                visited.append(current)
                L = current.fci

                RAR = rule_miner.mine_RAR(L, S, 0.95, 1.0, 0.95, 1.0)
                nb_consequent = len(rule_miner.mine_CAR2(L, S, RAR, analyzer))
                nb_basic_rules += len(RAR)
                nb_rules += nb_consequent

                print('  - L:' + str(L.closure) + ',gen: ' + str(L.generators) + ', nb BR min/max: ' + str(
                    len(RAR)) + ', nb CR: ' + str(nb_consequent) + ', TBR: ' + str(nb_basic_rules) + ', TBC: ' + str(
                    nb_rules))

                for child in current.children:
                    for grandchild in child.children:
                        if grandchild not in to_extract and grandchild not in visited:
                            to_extract.append(grandchild)
                        else:
                            print('Child: ' + str(grandchild.fci.closure) + ', gen: ' +  str(grandchild.fci.generators) + ' already waiting for extraction or visited')

        print('nb rules: ' + str(nb_rules))
        self.assertTrue(False)