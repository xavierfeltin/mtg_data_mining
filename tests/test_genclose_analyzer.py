import unittest
from genclose_analyzer import GenCloseAnalyzer as GCA
from genclose_analyzer import RulesAssociationMaximalConstraintMiner as RAMCM
from genclose_analyzer import is_in_generators
from genclose_analyzer import Rule

class TestGenCloseAnalyzer(unittest.TestCase):
    def setUp(self):
        """
        Validate the developments with the indications published here:
        https://pdfs.semanticscholar.org/56a4/ec156b26225b5922182bacc4c5b26fd5a555.pdf
        """

        self.db = []
        self.db.append(['a','b','c','e','g','h'])
        self.db.append(['a','c','d','f','h'])
        self.db.append(['a','d','e','f','g','h'])
        self.db.append(['b','c','e','f','g','h'])
        self.db.append(['b','c','e'])
        self.db.append(['b','c'])

        self.db_rules = [] #database used for rules association mining
        self.db_rules.append(['a', 'c', 'e', 'g', 'i'])
        self.db_rules.append(['a', 'c', 'f', 'h', 'i'])
        self.db_rules.append(['a', 'd', 'f', 'h', 'i'])
        self.db_rules.append(['b', 'c', 'e', 'g', 'i'])
        self.db_rules.append(['a', 'c', 'e', 'g', 'i'])
        self.db_rules.append(['b', 'c', 'e', 'g', 'i'])
        self.db_rules.append(['a', 'c', 'f', 'h', 'i'])

        self.db_rules_integer = []  # database used for rules association mining with integer
        self.db_rules_integer.append([1, 3, 5, 7, 9])
        self.db_rules_integer.append([1, 3, 6, 8, 9])
        self.db_rules_integer.append([1, 4, 6, 8, 9])
        self.db_rules_integer.append([2, 3, 5, 7, 9])
        self.db_rules_integer.append([1, 3, 5, 7, 9])
        self.db_rules_integer.append([2, 3, 5, 7, 9])
        self.db_rules_integer.append([1, 3, 6, 8, 9])

        self.analyzer = GCA([], 1)
        root = None

        a = GCA.Node(3, ('a'), ['a'], (1,2,3),root)
        b = GCA.Node(4, ('b'), ['b'], (1,4,5,6),root)
        c = GCA.Node(5, ('c'), ['c'], (1,2,4,5,6),root)
        d = GCA.Node(2, ('d'), ['d'], (2,3),root)
        e = GCA.Node(4, ('e'), ['e'], (1,3,4,5),root)
        f = GCA.Node(3, ('f'), ['f'], (2,3,4),root)
        g = GCA.Node(3, ('g'), ['g'], (1,3,4),root)
        h = GCA.Node(4, ('h'), ['h'], (1,2,3,4),root)
        self.L1 = [d,a,f,g,b,e,h,c]

        dc = GCA.Node(1, ('a','d','f','h','c'), ['d','c'], set([2]), d)
        de = GCA.Node(1, ('a', 'd', 'f', 'h', 'e'), ['d', 'e'], set([3]), d)
        dg = GCA.Node(1, ('a', 'd', 'f', 'h', 'e', 'g'), ['d', 'g'], set([3]), d)
        af = GCA.Node(2, ('a','f','h'),['a','f'], (2,3), a)
        ag = GCA.Node(2, ('a','h','e','g'),['a','g'], (1,3), a)
        ab = GCA.Node(1, ('a','h','b','c'),['a','b'], set([1]), a)
        ac = GCA.Node(2, ('a','h','c'),['a','c'], (1,2), a)
        ae = GCA.Node(2, ('a','e'),['a','e'], (1,3), a)
        gb = GCA.Node(2, ('e','g','h','b','c'),['g','b'], (1,4), g)
        gc = GCA.Node(2, ('g','c'),['g','c'], (1,4), g)
        be = GCA.Node(3, ('b','c','e'),['b','e'], (1,4,5), b)
        bh = GCA.Node(2, ('b','c','h'),['b','h'], (1,4), b)
        eh = GCA.Node(3, ('e','h'),['e','h'], (1,3,4), e)
        ec = GCA.Node(3, ('e','c'),['e','c'], (1,4,5), e)
        fg = GCA.Node(2, ('f','h','e','g'),['f','g'], (3,4), f)
        fb = GCA.Node(1, ('f','h','b','c'),['f','b'], set([4]), f)
        fc = GCA.Node(2, ('f','h','c'),['f','c'], (2,4), f)
        fe = GCA.Node(2, ('f','h','e'),['f','e'], (3,4), f)
        hc = GCA.Node(3, ('h','c'),['h','c'], (1,2,4), h)

        #Order here is important, it depends of the order at L1
        self.L2 = [dg,de,dc,af,ag,ab,ae,ac,fg,fb,fe,fc,gb,gc,be,bh,eh,ec,hc]

    def test_attribute_folders_L1(self):
        self.analyzer.attribute_folders(self.L1, 1)
        self.assertEqual(len(self.analyzer.L_folders), len(self.L1))

    def test_attribute_folders_L2(self):
        self.analyzer.attribute_folders(self.L2, 2)
        folders = self.analyzer.L_folders
        self.assertEqual(len(folders[GCA.key_folder(['a'])]), 5)
        self.assertEqual(len(folders[GCA.key_folder(['b'])]), 2)
        self.assertEqual(len(folders[GCA.key_folder(['d'])]), 3)
        self.assertEqual(len(folders[GCA.key_folder(['e'])]), 2)
        self.assertEqual(len(folders[GCA.key_folder(['f'])]), 4)
        self.assertEqual(len(folders[GCA.key_folder(['g'])]), 2)
        self.assertEqual(len(folders[GCA.key_folder(['h'])]), 1)
        self.assertNotIn(GCA.key_folder(['c']), folders)

    def test_EOB_L1(self):
        self.analyzer.attribute_folders(self.L1,1)
        self.analyzer.extend_merge(self.L1,1)
        self.assertEqual(len(self.analyzer.L_folders), len(self.L1))

    def test_EOB_L2(self):
        self.analyzer.attribute_folders(self.L2,2)
        self.analyzer.extend_merge(self.L2,2)
        folders = self.analyzer.L_folders

        self.assertEqual(len(self.analyzer.L_folders), 5)

        self.assertEqual(len(folders[GCA.key_folder(['d'])]), 2)
        self.assertEqual(len(folders[GCA.key_folder(['a'])]), 4)
        self.assertEqual(len(folders[GCA.key_folder(['g'])]), 3)
        self.assertEqual(len(folders[GCA.key_folder(['f'])]), 3)
        self.assertEqual(len(folders[GCA.key_folder(['h'])]), 1)

        folder = folders[GCA.key_folder(['d'])]
        self.assertEqual(folder[0].closure,frozenset(('a','d','f','g','h','e','g')))
        self.assertEqual(folder[0].generators, [['d','g'], ['d','e']])
        self.assertEqual(folder[0].transactions,set([3]))
        self.assertEqual(folder[0].support, 1)
        self.assertEqual(folder[1].closure, frozenset(('a','d','f','h','c')))
        self.assertEqual(folder[1].generators, [['d','c']])
        self.assertEqual(folder[1].transactions, set([2]))
        self.assertEqual(folder[1].support, 1)

        folder = folders[GCA.key_folder(['a'])]
        self.assertEqual(folder[0].closure, frozenset(('a','h','f')))
        self.assertEqual(folder[0].generators, [['a', 'f']])
        self.assertEqual(folder[0].transactions, set([2,3]))
        self.assertEqual(folder[0].support, 2)
        self.assertEqual(folder[1].closure, frozenset(('a','h','e','g')))
        self.assertEqual(folder[1].generators, [['a','g'], ['a','e']])
        self.assertEqual(folder[1].transactions, set([1, 3]))
        self.assertEqual(folder[1].support, 2)
        self.assertEqual(folder[2].closure, frozenset(('a','h','b','c','e','g')))
        self.assertEqual(folder[2].generators, [['a', 'b']])
        self.assertEqual(folder[2].transactions, set([1]))
        self.assertEqual(folder[2].support, 1)
        self.assertEqual(folder[3].closure, frozenset(('a','h','c')))
        self.assertEqual(folder[3].generators, [['a','c']])
        self.assertEqual(folder[3].transactions, set([1,2]))
        self.assertEqual(folder[3].support, 2)

        folder = folders[GCA.key_folder(['g'])]
        self.assertEqual(folder[0].closure, frozenset(('e','g','h','b','c')))
        self.assertEqual(folder[0].generators, [['g','b'],['g','c'],['b','h']])
        self.assertEqual(folder[0].transactions, set([1, 4]))
        self.assertEqual(folder[0].support, 2)
        self.assertEqual(folder[1].closure, frozenset(('b', 'c', 'e')))
        self.assertEqual(folder[1].generators, [['b', 'e'], ['e', 'c']])
        self.assertEqual(folder[1].transactions, set([1,4,5]))
        self.assertEqual(folder[1].support, 3)
        self.assertEqual(folder[2].closure, frozenset(('e', 'h')))
        self.assertEqual(folder[2].generators, [['e', 'h']])
        self.assertEqual(folder[2].transactions, set([1, 3, 4]))
        self.assertEqual(folder[2].support, 3)

        folder = folders[GCA.key_folder(['f'])]
        self.assertEqual(folder[0].closure, frozenset(('f', 'h', 'e', 'g')))
        self.assertEqual(folder[0].generators, [['f', 'g'], ['f', 'e']])
        self.assertEqual(folder[0].transactions, set([3, 4]))
        self.assertEqual(folder[0].support, 2)
        self.assertEqual(folder[1].closure, frozenset(('f','h','b','c','e','g')))
        self.assertEqual(folder[1].generators, [['f', 'b']])
        self.assertEqual(folder[1].transactions, set([4]))
        self.assertEqual(folder[1].support, 1)
        self.assertEqual(folder[2].closure, frozenset(('f', 'h', 'c')))
        self.assertEqual(folder[2].generators, [['f', 'c']])
        self.assertEqual(folder[2].transactions, set([2,4]))
        self.assertEqual(folder[2].support, 2)

    def test_mine(self):
        analyzer = GCA(self.db, 0.16) #percentage to get a min_supp of 1 matching the publication
        analyzer.clean_database()
        analyzer.mine()
        #closed_items = analyzer.lcg_into_list() for double hash

        db_size = len(self.db)

        expected_LGC = []
        expected_LGC.append(GCA.Node(2/db_size,set(['a','d','f','h']),[['d'],['a','f']],None))
        expected_LGC.append(GCA.Node(3/db_size,set(['a','h']),[['a']],None))
        expected_LGC.append(GCA.Node(3/db_size,set(['f','h']),[['f']],None))
        expected_LGC.append(GCA.Node(3/db_size,set(['e','g','h']),[['g'],['e','h']],None))
        expected_LGC.append(GCA.Node(4/db_size,set(['b','c']),[['b']],None))
        expected_LGC.append(GCA.Node(4/db_size,set(['e']),[['e']],None))
        expected_LGC.append(GCA.Node(4/db_size,set(['h']),[['h']],None))
        expected_LGC.append(GCA.Node(5/db_size,set(['c']),[['c']],None))
        expected_LGC.append(GCA.Node(1/db_size,set(['a','d','f','h','e','g']),[['d','g'],['d','e'],['a','f','g'],['a','f','e']],None))
        expected_LGC.append(GCA.Node(1/db_size,set(['a','d','f','h','c']),[['d','c'], ['a','f','c']],None))

        #TODO: check with publication's authors since aheg appears in two transactions in the database.
        #TODO: the example illustration shows an error with support of 1 but two transactions 1 and 3
        #expected_LGC.append(GCA.Node(1,set(['a','h','e','g']),[['a','g'],['a','e']],None))

        expected_LGC.append(GCA.Node(2/db_size,set(['a','h','e','g']),[['a','g'],['a','e']],None))
        expected_LGC.append(GCA.Node(1/db_size,set(['a','h','b','c','e','g']),[['a','b'],['a','g','c'],['a','e','c']],None))
        expected_LGC.append(GCA.Node(2/db_size,set(['a','h','c']),[['a','c']],None))
        expected_LGC.append(GCA.Node(2/db_size,set(['f','h','e','g']),[['f','g'],['f','e']],None))
        expected_LGC.append(GCA.Node(1/db_size,set(['f','h','b','c','e','g']),[['f','b'],['f','g','c'],['f','e','c']],None))
        expected_LGC.append(GCA.Node(2/db_size,set(['f','h','c']),[['f','c']],None))
        expected_LGC.append(GCA.Node(2/db_size,set(['e','g','h','b','c']),[['g','b'],['g','c'],['b','h'],['c','e','h']],None))
        expected_LGC.append(GCA.Node(3/db_size,set(['b','c','e']),[['b','e'],['c','e']],None))
        expected_LGC.append(GCA.Node(3/db_size,set(['h','c']),[['h','c']],None))

        #TODO: check with publication's authors if it is a mistake that afc is seperated from dc
        #TODO: since they have the same closure and the same support
        #expected_LGC.append(GCA.Node(1,set(['a','h','f','c','d']),[['a','f','c']],None))

        for index,expected in enumerate(expected_LGC):
            #check closure
            match = analyzer.search_node_with_closure(expected.closure)
            self.assertSequenceEqual(expected.closure, match.closure)

            #check support
            self.assertEqual(expected.support, match.support)

            #check generators
            for generator in expected.generators:
                match = analyzer.search_node_with_generator(None, generator)
                self.assertIsNotNone(match)

        self.assertEqual(len(expected_LGC),len(analyzer.lcg_into_list()))

    def test_mine_db_rules(self):
        analyzer = GCA(self.db_rules, 1/7)  #percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        self.assertEqual(len(analyzer.lcg_into_list()), 10)

        expected_LGC = []
        expected_LGC.append(GCA.Node(2/7, set(['a', 'c', 'e', 'g', 'i']), [['a','e'], ['a', 'g']], None))
        expected_LGC.append(GCA.Node(2/7, set(['b', 'c','e','g','i']), [['b']], None))
        expected_LGC.append(GCA.Node(2/7, set(['a', 'c','f','h','i']), [['c','f'],['c','h']], None))
        expected_LGC.append(GCA.Node(1/7, set(['a', 'd','f','h','i']), [['d']], None))
        expected_LGC.append(GCA.Node(4/7, set(['c', 'e', 'g','i']), [['e'], ['g']], None))
        expected_LGC.append(GCA.Node(4/7, set(['a', 'c', 'i']), [['a','c']], None))
        expected_LGC.append(GCA.Node(3/7, set(['a', 'f','h','i']), [['f'],['h']], None))
        expected_LGC.append(GCA.Node(6/7, set(['c', 'i']), [['c']], None))
        expected_LGC.append(GCA.Node(5/7, set(['a', 'i']), [['a']], None))
        expected_LGC.append(GCA.Node(7/7, set(['i']), [['i']], None))

        for index,expected in enumerate(expected_LGC):
            #check closure
            match = analyzer.search_node_with_closure(expected.closure)
            self.assertSequenceEqual(expected.closure, match.closure)

            #check support
            self.assertEqual(expected.support, match.support)

            #check generators
            for generator in expected.generators:
                match = analyzer.search_node_with_generator(None, generator)
                self.assertIsNotNone(match)

    def test_MFCS_FromLattice(self):
        analyzer = GCA(self.db_rules, 1/7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['a','c','f','h','i']), rule_miner._get_support(set(['a','c','f','h','i'])),1/7, 1)

        self.assertEqual(len(lcg_S), 6)

        expected_LGC = []
        expected_LGC.append(GCA.Node(2/7, set(['a', 'c', 'f', 'h', 'i']), [['c', 'f'], ['c', 'h']], None))
        expected_LGC.append(GCA.Node(4/7, set(['a', 'c', 'i']), [['a', 'c']], None))
        expected_LGC.append(GCA.Node(3/7, set(['a', 'f', 'h', 'i']), [['f'], ['h']], None))
        expected_LGC.append(GCA.Node(6/7, set(['c', 'i']), [['c']], None))
        expected_LGC.append(GCA.Node(5/7, set(['a', 'i']), [['a']], None))
        expected_LGC.append(GCA.Node(7/7, set(['i']), [['i']], None))

        for index, expected in enumerate(expected_LGC):
            # check closure
            match = analyzer.search_node_with_closure(expected.closure, lcg_S)
            self.assertSequenceEqual(expected.closure, match.closure)

            # check support
            self.assertEqual(expected.support, match.support)

            # check generators
            for generator in expected.generators:
                self.assertTrue(is_in_generators(generator, match.generators, True))

    def test_MFS_RestrictMaxSC_1(self):
        # From publication example 3.a
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['c', 'e', 'a', 'g', 'i']), 2/7, 1/7, 1)

        #Enumerate left side
        Y = set(['c','e','g'])
        X = set([])
        Z1 = set(['c','e','g'])
        match = analyzer.search_node_with_closure(Y, lcg_S)
        gen_X_Y = match.generators
        fs_star_Y = rule_miner.MFS_RestrictMaxSC(Y, X, Z1, gen_X_Y)

        self.assertEqual(len(fs_star_Y), 6)
        expected_itemsets = []
        expected_itemsets.append(set(['e']))
        expected_itemsets.append(set(['e','c']))
        expected_itemsets.append(set(['e','g']))
        expected_itemsets.append(set(['e','c','g']))
        expected_itemsets.append(set(['g']))
        expected_itemsets.append(set(['g','c']))
        for itemset in expected_itemsets:
            self.assertIn(itemset, fs_star_Y)

        #Enumerate right side in accordance with left hand side 'e'
        Y = frozenset(['c', 'e', 'a', 'g', 'i']).difference(frozenset('e'))
        X = set(['e'])
        Z1 = set(['a', 'i'])
        match = analyzer.search_node_with_closure(Y, lcg_S)
        gen_X_Y = match.generators
        fs_star_Y = rule_miner.MFS_RestrictMaxSC(Y, X, Z1, gen_X_Y)

        self.assertEqual(len(fs_star_Y), 2)
        expected_itemsets = []
        expected_itemsets.append(set(['a']))
        expected_itemsets.append(set(['a', 'i']))
        for itemset in expected_itemsets:
            self.assertIn(itemset, fs_star_Y)

    def test_MFS_RestrictMaxSC_2(self):
        # From publication example 3.b
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['a', 'c', 'f', 'h', 'i']), 2/7, 1/7, 1)

        # Enumerate left side
        Y = set(['a'])
        X = set([])
        Z1 = set(['a'])
        match = analyzer.search_node_with_closure(Y, lcg_S)
        gen_X_Y = match.generators
        fs_star_Y = rule_miner.MFS_RestrictMaxSC(Y, X, Z1, gen_X_Y)

        self.assertEqual(len(fs_star_Y), 1)
        expected_itemsets = []
        expected_itemsets.append(set(['a']))
        for itemset in expected_itemsets:
            self.assertIn(itemset, fs_star_Y)

        # Enumerate right side in accordance with left hand side 'a'
        Y = frozenset(['a', 'c', 'f', 'h', 'i']).difference(frozenset('a'))
        X = set(['a'])
        Z1 = set(['c', 'f', 'h', 'i'])
        match = analyzer.search_node_with_closure(Y, lcg_S)
        gen_X_Y = match.generators
        fs_star_Y = rule_miner.MFS_RestrictMaxSC(Y, X, Z1, gen_X_Y)

        self.assertEqual(len(fs_star_Y), 6)
        expected_itemsets = []
        expected_itemsets.append(set(['c', 'f']))
        expected_itemsets.append(set(['c', 'f', 'i']))
        expected_itemsets.append(set(['c', 'f', 'h']))
        expected_itemsets.append(set(['c', 'f', 'h', 'i']))
        expected_itemsets.append(set(['c', 'h']))
        expected_itemsets.append(set(['c', 'h', 'i']))
        for itemset in expected_itemsets:
            self.assertIn(itemset, fs_star_Y)

    def test_MAR_MaxSC_OneClass(self):

        # From publication example 3.a
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['c', 'e', 'a', 'g', 'i']), 2 / 7, 1 / 7, 1)

        # Generate rules for S_star_S1 = set(['c', 'e', 'a', 'g', 'i'])
        L_C1 = set(['c','e','g'])
        match = analyzer.search_node_with_closure(L_C1, lcg_S)

        gen_L_C1 = match.generators
        R1 = set(['a', 'i'])
        S_star_S1 = set(['c', 'e', 'a', 'g', 'i'])
        match = analyzer.search_node_with_closure(S_star_S1, lcg_S)
        gen_S_star_S1 = match.generators
        S1 = set(['c', 'e', 'a', 'g', 'i'])

        rules = rule_miner.MAR_MaxSC_OneClass(L_C1, gen_L_C1, R1, S_star_S1, gen_S_star_S1, S_star_S1)

        self.assertEqual(len(rules), 12)
        expected_rules = []
        expected_rules.append(Rule(set(['e']), set(['a'])))
        expected_rules.append(Rule(set(['e']), set(['a','i'])))
        expected_rules.append(Rule(set(['c','e']), set(['a'])))
        expected_rules.append(Rule(set(['c','e']), set(['a','i'])))
        expected_rules.append(Rule(set(['e','g']), set(['a'])))
        expected_rules.append(Rule(set(['e','g']), set(['a','i'])))
        expected_rules.append(Rule(set(['c','e','g']), set(['a'])))
        expected_rules.append(Rule(set(['c','e','g']), set(['a','i'])))
        expected_rules.append(Rule(set(['g']), set(['a'])))
        expected_rules.append(Rule(set(['g']), set(['a','i'])))
        expected_rules.append(Rule(set(['c','g']), set(['a'])))
        expected_rules.append(Rule(set(['c','g']), set(['a','i'])))

    def test_MAR_MaxSC_OneClass_2(self):

        # From publication example 3.b
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['a', 'c', 'f', 'h', 'i']), 2 / 7, 1 / 7, 1)

        # Generate rules for S_star_S1 = set(['c', 'e', 'a', 'g', 'i'])
        L_C1 = set(['a'])
        match = analyzer.search_node_with_closure(L_C1, lcg_S)
        gen_L_C1 = match.generators
        R1 = set(['c', 'f', 'h', 'i'])
        S_star_S1 = set(['a', 'c', 'f', 'h', 'i'])
        match = analyzer.search_node_with_closure(S_star_S1, lcg_S)
        gen_S_star_S1 = match.generators
        S1 = set(['a', 'c', 'f', 'h', 'i'])

        rules = rule_miner.MAR_MaxSC_OneClass(L_C1, gen_L_C1, R1, S_star_S1, gen_S_star_S1, S_star_S1)

        self.assertEqual(len(rules), 6)
        expected_rules = []
        expected_rules.append(Rule(set(['a']), set(['c','f'])))
        expected_rules.append(Rule(set(['a']), set(['c','f','i'])))
        expected_rules.append(Rule(set(['a']), set(['c','f','h'])))
        expected_rules.append(Rule(set(['a']), set(['c','f','h','i'])))
        expected_rules.append(Rule(set(['a']), set(['c','h'])))
        expected_rules.append(Rule(set(['a']), set(['c','h','i'])))

    def test_MAR_MaxSC_OneClass_3(self):

        # From publication example 1.c
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['a', 'c', 'f', 'h', 'i']), 2 / 7, 1 / 7, 1)

        # Generate rules for S_star_S1 = set(['c', 'e', 'a', 'g', 'i'])
        L_C1 = set(['a'])
        match = analyzer.search_node_with_closure(L_C1, lcg_S)
        gen_L_C1 = match.generators
        R1 = set(['c', 'f', 'h', 'i'])
        S_star_S1 = set(['a', 'f', 'h', 'i'])
        match = analyzer.search_node_with_closure(S_star_S1, lcg_S)
        gen_S_star_S1 = match.generators
        S1 = set(['a', 'c', 'f', 'h', 'i'])

        rules = rule_miner.MAR_MaxSC_OneClass(L_C1, gen_L_C1, R1, S_star_S1, gen_S_star_S1, S_star_S1)

        self.assertEqual(len(rules), 6)
        expected_rules = []
        expected_rules.append(Rule(set(['a']), set(['f'])))
        expected_rules.append(Rule(set(['a']), set(['f', 'i'])))
        expected_rules.append(Rule(set(['a']), set(['h'])))
        expected_rules.append(Rule(set(['a']), set(['h', 'i'])))
        expected_rules.append(Rule(set(['a']), set(['f', 'h'])))
        expected_rules.append(Rule(set(['a']), set(['f', 'h', 'i'])))

    def test_MAR_MaxSC_OneClass_4(self):

        # From publication example 3.a
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        rule_miner = RAMCM(analyzer.lcg_into_list())
        lcg_S = rule_miner.MFCS_FromLattice(rule_miner.lcg, set(['c', 'e', 'a', 'g', 'i']), 2/7, 1/7, 5/7)

        # Generate rules for S_star_S1 = set(['c', 'e', 'a', 'g', 'i'])
        L_C1 = set(['c', 'e', 'g'])
        match = analyzer.search_node_with_closure(L_C1, lcg_S)
        gen_L_C1 = match.generators
        R1 = set(['a', 'i'])
        S_star_S1 = set(['a', 'c', 'i'])
        match = analyzer.search_node_with_closure(S_star_S1, lcg_S)
        gen_S_star_S1 = match.generators
        S1 = set(['c', 'e', 'a', 'g', 'i'])

        rules = rule_miner.MAR_MaxSC_OneClass(L_C1, gen_L_C1, R1, S_star_S1, gen_S_star_S1, S_star_S1)

        self.assertEqual(len(rules), 2)
        expected_rules = []

    def test_mine_rules_1(self):
        # From publication example 3.a
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        L1 = set({'c','e','g'})
        R1 = set(['a','i'])
        rule_miner = RAMCM(analyzer.lcg_into_list())
        rule_miner.mine(1/7,5/7,1/3,0.9,L1,R1)

        self.assertEqual(len(rule_miner.ars),14)

    def test_mine_rules_2(self):
        # From publication example 3.b
        analyzer = GCA(self.db_rules, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        L1 = set({'a'})
        R1 = set(['c','f', 'h', 'i'])
        rule_miner = RAMCM(analyzer.lcg_into_list())
        rule_miner.mine(1/7,5/7,1/3,0.9,L1,R1)

        self.assertEqual(len(rule_miner.ars),12)

    def test_mine_rules_1_integer(self):
        analyzer = GCA(self.db_rules_integer, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        L1 = set({3, 5, 7})
        R1 = set([1, 9])
        rule_miner = RAMCM(analyzer.lcg_into_list())
        rule_miner.mine(1 / 7, 5 / 7, 1 / 3, 0.9, L1, R1)

        self.assertEqual(len(rule_miner.ars), 14)

    def test_mine_rules_2_integer(self):
        # From publication example 3.b
        analyzer = GCA(self.db_rules_integer, 1 / 7)  # percentage indicated in publication
        analyzer.clean_database()
        analyzer.mine()

        L1 = set({1})
        R1 = set([3, 6, 8, 9])
        rule_miner = RAMCM(analyzer.lcg_into_list())
        rule_miner.mine(1 / 7, 5 / 7, 1 / 3, 0.9, L1, R1)

        self.assertEqual(len(rule_miner.ars), 12)

