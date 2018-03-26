import hashlib
from tqdm import tqdm
from collections import OrderedDict
from itertools import combinations
from operator import itemgetter

#Utilities
def reverse_enumerate(iterable):
    """
    Enumerate over an iterable in reverse order while retaining proper indexes
    source: http://galvanist.com/post/53478841501/python-reverse-enumerate
    """
    return zip(reversed(range(len(iterable))), reversed(iterable))

def get_list_intersection(left_gen, right_gen):
    intersection = []
    for gen in left_gen:
        if gen in right_gen:
            intersection.append(gen)
    return intersection

class GenCloseAnalyzer:
    """
    Mine closed itemsets and associated generators
    Generate association rules from mined itemsets

    Bibliography :
    - Simultaneous mining of frequent closed itemsets and their generators: Foundation and Algorithm, 2014
    source : https://pdfs.semanticscholar.org/56a4/ec156b26225b5922182bacc4c5b26fd5a555.pdf
    """

    class Node:
        """
        Data structure to manage node in the tree of closed items
        """
        def __init__(self, support, closure, generators, transactions=None, left_parent=None, right_parent=None):
            """
            Init
            :param support: support of the itemset
            :param closure: closure of the itemset (closed if hG = h(G)
            :param generators: set of generators from the join of two parent nodes
            value is a list when building tree or a list of list when the node is inserted into LCG.
            :param transactions: set of transactions from the intersection of the two parent nodes.
            value is None when the node is inserted into LCG.
            :param left_parent: parent node
            """
            self.support = support
            if isinstance(closure,int):
                self.closure = set([closure])
            else:
                self.closure = set(closure)

            self.i_generator = None #i_generator used for merging with other nodes. Generators are list, order is important
            self.generators = [] #All generators for the node. Generators are list, order is important

            if len(generators) > 0 and isinstance(generators[0], list):
                for generator in generators:
                    self.generators.append(generator)
                self.i_generator = generators[0]
            else:
                self.generators.append(generators)
                self.i_generator = generators

            if transactions is not None:
                self.transactions = set(transactions)
            else:
                self.transactions = None

            self.diffset = []
            self.key = 0 #hash key based on sum transactions
            self.folder = None
            self.left_parent = left_parent
            self.right_parent = right_parent

        def get_sum_transaction(self):
            """
            Return the sum of transactions index for hashing in LCG
            :return: sum
            """
            return sum(self.transactions)

    def __init__(self, database, min_support = 1.0):
        self.database = database
        self.db_length = len(self.database)
        self.ratio_min_supp = min_support
        self.min_supp = round(len(self.database) * self.ratio_min_supp)
        self.sorted_items = None
        self.reverse_db = {} #fast access to transactions containing a particular item
        self.L_folders = {} #folders regrouping nodes with common prefixes
        self.LCG = {} #double hash store (transaction sum + support)
        #TODO: implement double hash with diffset
        #self.LCG = [] #double hash store (transaction sum + support)

    def lcg_into_list(self):
        """
        Return LCG as a list
        :return: list of all closed itemsets and their generators
        """
        list_closed = []
        for key_sum in self.LCG.keys():
            for key_supp, closed_list in self.LCG[key_sum].items():
                list_closed.extend(closed_list)

        list_closed = sorted(list_closed, key=lambda item: item.support)
        return list_closed

    def get_closed_items_closures(self):
        list_closures = []
        for key_sum in self.LCG.keys():
            for key_supp, closed_list in self.LCG[key_sum].items():
                for closed in closed_list:
                    list_closures.append(list(closed.closure))
        return list_closures

    def clean_database(self):
        """
        Return a list of items with a support greater than min_support
        :return: list of items
        """
        items = {}
        database_size = len(self.database)
        self.reverse_db.clear()

        # Scan the database to initialize the frequence of all items used in the transactions
        for index, transaction in enumerate(self.database):
            for item in transaction:
                if item in items:
                    items[item] += 1
                else:
                    items[item] = 1

        # Sort the items by increasing frequencies and renumerate the items (most frequent items = biggest number)
        # Skip the items with a frequency lower than the support
        self.sorted_items = {k: (v/database_size) for k, v in items.items() if v >= self.min_supp}
        self.sorted_items = OrderedDict(sorted(self.sorted_items.items(), key=itemgetter(1, 0), reverse=False))

        # Reduce the database size by ignoring non frequent items and empty transactions
        transactions = []
        for index, transaction in enumerate(self.database):
            list_items = []
            for item in transaction:
                if item in self.sorted_items:
                    list_items.append(item)

                    if item in self.reverse_db:
                        self.reverse_db[item].append(index)
                    else:
                        self.reverse_db[item] = [index]

            transactions.append(list_items)

        self.database = transactions
        self.db_length = len(self.database)

    def get_transactions_with_item(self, item):
        """
        Return a list of transactions containing the item
        :return: list of transactions
        """
        if isinstance(item, list):
            transactions = self.reverse_db[item[0]]
            for i in range(1,len(item)):
                transactions = frozenset(transactions).intersection(frozenset(self.reverse_db[item[i]]))
            return transactions
        else:
            return self.reverse_db[item]


    def extend_merge(self, tree_level, index_level):
        """
        Complete the closure of the nodes in the tree_level in parameters (operator EOB)
        :param tree_level: slice of the tree containing the nodes to complete
        :param index_level: current level index in the referential 1..N (and not 0..N-1)
        """
        for i in tqdm(range(len(tree_level)-1)):
            j = i+1
            while j < len(tree_level):
                X = tree_level[i]
                Y = tree_level[j]

                frozen_X = frozenset(X.transactions)
                frozen_Y = frozenset(Y.transactions)

                # Case 1: In the case that X.O C Y.O, we extend X.H by Y.H: X.H = X.H union Y.H.
                if frozen_X < frozen_Y:
                    X.closure = frozenset(X.closure).union(frozenset(Y.closure))
                    j += 1

                # Case 2: If X.O includes Y.O, we add X.H to Y.H.
                elif frozen_X > frozen_Y:
                    Y.closure = frozenset(Y.closure).union(frozenset(X.closure))
                    j += 1

                # Case 3: In the remaining case, this procedure merges Y to X. It pushes all generators in Y.GS to X.GS, adds Y.H to X.H, and discards Y
                elif frozen_X == frozen_Y:
                    #Recall that we join only i-generators of G1 and G2 ( in the nodes at L[i]),
                    # with common i-1 first items, called the common prefix.
                    i_generators = []
                    for generator in Y.generators:
                        if len(generator) == index_level \
                            and (len(frozenset(generator).difference(frozenset(X.i_generator))) == 1):
                            i_generators.append(generator)

                    if len(i_generators) > 0:
                        X.generators.extend(i_generators)
                        X.closure = frozenset(X.closure).union(frozenset(Y.closure))

                        X_key = GenCloseAnalyzer.key_folder(X.folder)
                        Y_key = GenCloseAnalyzer.key_folder(Y.folder)

                        # Hence, if Y is not in the same folder with X, we move all nodes that are in the folder containing
                        # Y to the folder containing X. Thus, X also has the prefixes of Y.
                        if Y_key != X_key:
                            for node in self.L_folders[Y_key]:
                                node.folder = X.folder
                                self.L_folders[X_key].append(node)
                            del self.L_folders[Y_key]

                        self.L_folders[X_key].remove(Y)
                        del tree_level[j]
                    else:
                        j += 1
                else:
                    #do nothing and process next item
                    j += 1

    def store_level(self, tree_level):
        """
        Save the closed items in the current tree level inside LCG
        :param tree_level: level to store
        :param lcg: store all the closed items
        """

        for node in tree_level:
            key = node.get_sum_transaction()
            if key in self.LCG:
                if node.support in self.LCG[key]:
                    existing_closed = self.LCG[key][node.support]
                    not_exist = True
                    for closed in existing_closed:
                        #If there exists itemset P in ℒ CG such that supp(P) = X.Supp and P includes or is equal to X.H,
                        # P is the closure that X.H wants to reach.Thus, the new generators in X.GS are pushed into
                        # the generator list of P and X.H becomes P.
                        if frozenset(closed.closure).issuperset(frozenset(node.closure)):
                            not_exist = False
                            for generator in node.generators:
                                if generator not in closed.generators:
                                    closed.generators.append(generator)
                            break

                    if not_exist:
                        self.LCG[key][node.support].append(GenCloseAnalyzer.Node(node.support, node.closure, node.generators, None, node.left_parent, node.right_parent))
                else:
                    self.LCG[key][node.support] = [GenCloseAnalyzer.Node(node.support, node.closure, node.generators, None, node.left_parent, node.right_parent)]
            else:
                self.LCG[key] = {}
                self.LCG[key][node.support] = [GenCloseAnalyzer.Node(node.support, node.closure,node.generators, None, node.left_parent, node.right_parent)]

        #TODO: implement double hash with diffset
        '''
        for node in tree_level:
            not_exist = True
            for closed in self.LCG:
                if closed.support == node.support and frozenset(closed.closure).issuperset(frozenset(node.closure)):
                    not_exist = False
                    for generator in node.generators:
                        if generator not in closed.generators:
                            closed.generators.append(generator)
                    break

            if not_exist:
                self.LCG.append(GenCloseAnalyzer.Node(node.support, node.closure,node.generators, None))
        '''

    @staticmethod
    def key_folder(key_list):
        """
        Generate a key to manage folders
        :param key_list: generator to convert in key
        :return: hashed key
        """
        return hashlib.md5(str(key_list).encode('utf-8')).hexdigest()

    def attribute_folders(self, tree_level, index_level):
        """
        Set the different node of the current level into folders
        :param tree_level: slice of the tree containing the nodes to complete
        :param index_level: current level index in the referential 1..N (and not 0..N-1)
        """
        self.L_folders.clear() #clean folders from previous level

        for node in tree_level:
            if index_level > 1:
                if GenCloseAnalyzer.key_folder(node.left_parent.i_generator) in self.L_folders:
                    self.L_folders[GenCloseAnalyzer.key_folder(node.left_parent.i_generator)].append(node)
                    node.folder = node.left_parent.i_generator
                else:
                    self.L_folders[GenCloseAnalyzer.key_folder(node.left_parent.i_generator)] = [node]
                    node.folder = node.left_parent.i_generator
            else:
                self.L_folders[GenCloseAnalyzer.key_folder(node.i_generator)] = [node]
                node.folder = node.i_generator

    def compute_diffset(self, node, left_parent):
        """
        Compute the diffset between the current node and it left parent
        :param node: current node
        :param left_parent: current node's left parent
        """
        return frozenset(left_parent.transactions).difference(frozenset(node.transactions))

    def update_node_diffset(self, node, left_parent):
        """
        Compute the diffset for the node and the left parent set in argument
        Use essentially for first level of the tree (left_parent will be the root)
        """
        diffset = self.compute_diffset(node, left_parent)
        node.support = left_parent.support - len(diffset)
        node.diffset.append(left_parent, diffset, node.generators)

        return diffset

    def get_common_left_parent(self, left, right):
        """
        Return the common left parent of two nodes
        :param left: left node to check
        :param right: right node to check
        :return: left parent or None if it does not exist
        """
        common_left_parent = None
        i = 0
        nb_diffsets = len(left.diffsets)
        while i < nb_diffsets and not common_left_parent:
            for right_diff in right.diffsets:
                if left.diffsets[i][0] == right_diff[0]:
                    common_left_parent = left.diffsets[i][0]
                    break
        return common_left_parent

    def update_diffset_join(self, node, left_parent, right_parent):
        """
        Define the diffset from joining the left and right node.
        Update only of they have a common left parent
        Use essentially for levels after the first one in the tree
        :param node: node to update
        :param left_parent: left node to join
        :param right_parent: right node to join
        """
        common_left_parent = self.get_common_left_parent(left_parent, right_parent)
        if common_left_parent is not None:
            merge_diffset = frozenset(self.compute_diffset(right_parent, common_left_parent)).difference(self.compute_diffset(right_parent, common_left_parent))
            node.support = left_parent.support - len(merge_diffset)
            node.diffset.append(left_parent, merge_diffset, node.generators) #TODO: node.generators may be not correct here => publication says GSj is the set of generators generated from left parents

    def search_node_with_generator(self, node, generator):
        """
        Return closure containing the generator given in argument
        :param node: left parent
        :param generator: generator to search in closed items in LCG
        :return: node or None if not found
        """

        transactions = self.get_transactions_with_item(generator)
        key_sum = sum(transactions)
        support = len(transactions)/self.db_length

        if key_sum in self.LCG:
            if support in self.LCG[key_sum]:
                for closed in self.LCG[key_sum][support]:
                    for gen in closed.generators:
                        if frozenset(gen) == frozenset(generator):
                            return closed
        return None


        #TODO: implement double hash with diffset
        '''
        for closed in self.LCG:
            for gen in closed.generators:
                if frozenset(gen) == frozenset(generator):
                    return closed
        return None
        '''

    def search_node_with_closure(self, search, lcg = []):
        # TODO: implement double hash with diffset
        if len(lcg) == 0:
            lcg = self.lcg_into_list()

        '''
        for closed in lcg:
            if frozenset(search) == frozenset(closed.closure):
                return closed
        return None
        '''

        for closed in reversed(lcg):
            if frozenset(search).issubset(frozenset(closed.closure)):
                return closed
        return None

    def mine(self):
        """
        Mine the closed itemsets of the database and the associated generators
        :return: list of nodes <closed itemset, support, generators>
        """
        print('Clean database function of support')
        self.clean_database()

        frequent_items = self.sorted_items.keys()
        lcg = []
        tree = []
        has_new_level = True
        i = 0 # 0 refers to L1

        # Initialiation of layer L1 in the tree
        print('Initialize first layer')
        LCurrent = []
        for item in frequent_items:
            associated_transactions = self.get_transactions_with_item(item)
            LCurrent.append(GenCloseAnalyzer.Node(len(associated_transactions)/self.db_length, item, [item], associated_transactions)) #<support, item, generators, transactions>
        tree.append(LCurrent)

        # Mine the itemsets and generators
        while has_new_level:
            print('L' + str(i + 1) + ': Attribute folders')
            self.attribute_folders(LCurrent,i+1) #dispatch items into folders

            print('L' + str(i + 1) + ': Extend merge (EOB)')
            self.extend_merge(LCurrent,i+1) #using EOB (complete function of the nodes of the same level

            print('L' + str(i+1) + ': Store ' + str(len(LCurrent)) + ' items (EOC)')
            self.store_level(LCurrent) #store the closed itemsets and generators inside LCG

            LNext = []

            print('L' + str(i + 1) + ': Generate new level by join (EOA)')
            if i > 0:
                for key, nodes in self.L_folders.items():
                    for left_index, left_node in enumerate(nodes):
                        for right_index, right_node in reverse_enumerate(nodes):
                            if left_index < right_index:
                                self.join(left_node, right_node, LNext, i)
                            else:
                                break
            else: #no folder in common for the first level of the tree
                for left_index, left_node in enumerate(LCurrent):
                    for right_index, right_node in reverse_enumerate(LCurrent):
                        if left_index < right_index:
                            self.join(left_node, right_node, LNext, i)
                        else:
                            break

            if len(LNext) == 0: has_new_level = False
            LCurrent = LNext
            i += 1
        return lcg

    def join(self, left_node, right_node, next_level, current_index):
        """
        utility method to package common code
        """
        new_transactions = frozenset(left_node.transactions).intersection(frozenset(right_node.transactions))
        new_support = len(new_transactions)/self.db_length

        if new_support != left_node.support and new_support != right_node.support and new_support >= self.ratio_min_supp:
            new_closure = frozenset(left_node.closure).union(frozenset(right_node.closure))  # using EOA
            self.join_generators(left_node, right_node, new_transactions, new_support, new_closure, next_level, current_index + 1)  # using Condition (5)

    def join_generators(self, left_node, right_node, new_transactions, new_support, new_closure, next_level, index_level):
        """
        Build the L[i+1] level by joining generators from L[i]
        :param left_node: node to merge
        :param right_node: node to merge
        :param new_transactions: list of transactions matching the left and right nodes
        :param new_support: support of the new_transactions
        :param new_closure: new closure matching the left and right nodes
        :param tree_next_level: Level in the tree for the new node
        :param index_level: current tree level processed in referential 1..N (not 0..N-1)
        :return: None
        """
        new_generators_set = []
        for left_gen in left_node.generators:
            for right_gen in right_node.generators:
                if len(left_gen) == index_level \
                        and len(right_gen) == index_level \
                        and len(frozenset(left_gen).intersection(frozenset(right_gen))) == (index_level-1):
                    generator_candidate = left_gen[:]
                    for generator in right_gen:
                        if generator not in generator_candidate:
                            generator_candidate.append(generator)
                    common_generators = get_list_intersection(left_gen, right_gen)
                    candidate_is_generator = True

                    for gen in common_generators:
                        subset_gen = generator_candidate[:]
                        subset_gen.remove(gen)
                        matching_node = self.search_node_with_generator(left_node, subset_gen)
                        if matching_node is None or new_support == matching_node.support:
                            candidate_is_generator = False
                            break #for each gen in common_generators
                        else:
                            #generator_candidate can be a generator
                            new_closure = frozenset(new_closure).union(frozenset(matching_node.closure)) #using EOA

                    if candidate_is_generator:
                        new_generators_set.append(generator_candidate)

        if len(new_generators_set) >= 1:
            #new i+1-generators
            next_level.append(GenCloseAnalyzer.Node(new_support, new_closure, new_generators_set, new_transactions, left_node, right_node))

def is_in_generators(searched_gen, list_generators, is_strict = False):
    set_search_gen = frozenset(searched_gen)
    for gen in list_generators:
        if is_strict:
            if set_search_gen == frozenset(gen):
                return True
        else:
            if set_search_gen.issubset(frozenset(gen)):
                return True
    return False

class RulesAssociationMaximalConstraintMiner:
    '''
    Rules association miner with configuration on items, support and confidence, based on the following publication:
    - Efficiently mining association rules based on maximum single constraints, Anh Tran, Tin C Truong, Bac Le, 2017
    source: https://link.springer.com/article/10.1007/s40595-017-0096-2
    '''

    class Rule:
        def __init__(self,left,right):
            self.left = left
            self.right = right

        def to_str(self):
            return  '+'.join([str(item) for item in self.left]) + '-->' + '+'.join([str(item) for item in self.right])

    def __init__(self, lcg):
        '''
        Initialize the rule association miner
        :param s0: minimal support
        :param s1: maximal support (1 is the common configuration)
        :param c0: minimal confidence
        :param c1: maximal confidence (1 is the common configuration)
        :param l1: constrained items for the left side of the rules
        :param r1: constrained items for the right side of the rules
        :param lcg: lattice of closed itemsets and their generators (with support)
        '''

        self.s0 = 0
        self.s1 = 1
        self.c0 = 0
        self.c1 = 1
        self.l1 = []
        self.r1 = []
        self.lcg = lcg
        self.ars = [] #list of mined rules

    def _get_support(self, itemset):
        '''
        Get the highest support from the lattice of closed generators
        The lattice is sorted by support.
        :param itemset: itemset to find the support
        :return: support of the itemset
        '''

        for closed in reversed(self.lcg):
            if frozenset(itemset).issubset(closed.closure):
                return closed.support
        return 0

    @staticmethod
    def get_minimals(X, Z1, gen_X_Y):
        '''
        Return Minimal{Rk = Sk\X | Sk belongs to G(X+Y), Rk included or equal to Z1}
        :return: array of minimals
        '''

        if len(gen_X_Y) == 0: return []

        minimals = []
        min_len = len(Z1)
        z1_combination = []
        for i in range(len(Z1)):
            z1_combination.extend(combinations(Z1, i + 1))
        z1_combination.append(frozenset([]))  # simulate empty element

        for Sk in gen_X_Y:
            Rk = frozenset(Sk).difference(frozenset(X))
            # if is_in_generators(Rk, gen_X_Y):
            if len(Rk) == 0:
                minimals.append(frozenset([]))
            else:
                found = False
                for comb in z1_combination:
                    if Rk == frozenset(comb):
                        found = True
                        break
                if found:
                    minimals.append(Rk)
                    if min_len > len(Rk):
                        min_len = len(Rk)

        for min in minimals:
            if len(min) > min_len:
                minimals.remove(min)

        return minimals

    def mine(self, s0, s1, c0, c1, l1, r1):
        '''
        Mine non redundant rules from LCG based on the constraints set in parameters
        :param s0: minimal support
        :param s1: maximal support (1 is the common configuration)
        :param c0: minimal confidence
        :param c1: maximal confidence (1 is the common configuration)
        :param l1: constrained items for the left side of the rules
        :param r1: constrained items for the right side of the rules
        '''

        self.ars = []
        if s0 > s1 or c0 > c1: return

        S1_star = frozenset(l1).union(frozenset(r1))
        C1 = l1
        supp_C1 = self._get_support(C1)

        #TODO: what is R0? not used after in algorithm...
        #R0_star = R0

        s0_star = max(s0, c0 * supp_C1)
        s1_star = s1

        fcs_S1_star = self.MFCS_FromLattice(self.lcg, S1_star, self._get_support(S1_star), s0_star, s1_star) #TODO: from examples looks like S = S1_star ...
        for S1_closed_item in fcs_S1_star:
            s0_prime = S1_closed_item.support/c1
            s1_prime = min(1, S1_closed_item.support/c0)

            lcg_s = self.MFCS_FromLattice(self.lcg, S1_closed_item.closure, S1_closed_item.support, 0, 1)
            fcs_C1 = self.MFCS_FromLattice(lcg_s, C1, supp_C1, s0_prime, s1_prime)
            for C1_closed_item in fcs_C1:
                AR_star = self.MAR_MaxSC_OneClass(C1_closed_item.closure, C1_closed_item.generators, r1,S1_closed_item.closure, S1_closed_item.generators, S1_closed_item.closure)  #TODO: from examples looks like S = S1_star ...
                self.ars.extend(AR_star)

    def MFCS_FromLattice(self, lcg, C1, supp_C1, s0, s1):
        '''
        Extract the frequent closed itemsets from LCG projected onto C1 and fulfilling the support constraint [s0,s1]
        :param lcg: lattice of closed generators
        :param C1: itemsets constraint
        :param supp_C1: support of C1
        :param s0: minimum support
        :param s1: maximum support
        :return: lcg projected onto C1
        '''

        fcs_C1 = []
        if s0 > s1 or supp_C1 > s1: return fcs_C1

        comb_Li = []
        for i in range(len(C1)):
            comb_Li.extend(combinations(C1, i + 1))

        for closed in lcg:
            generators_C1 = []
            if s0 <= closed.support <= s1:
                #if there is Li in G(L) and Li included or equal in C1 then

                for li in comb_Li:
                    #if frozenset(li).issubset(C1):
                    if is_in_generators(li, closed.generators, True):
                        generators_C1.append(list(li))

                if len(generators_C1) > 0:
                    L_C1 = frozenset(closed.closure).intersection(frozenset(C1))
                    fcs_C1.append(GenCloseAnalyzer.Node(closed.support, L_C1, generators_C1))
        return fcs_C1

    def MFS_RestrictMaxSC(self, Y, X, Z1, gen_X_Y):
        '''
        Compute frequent sub itemsets restricted on X with upper bound Z1
        Used to enumerate items of left and right side of the rules
        :param Y: closure that will be constrained on X
        :param X: itemset constraint with X intersect Y = empty set
        :param Z1: uppper bound and Z1 included or equal to Y, Z1 is not an empty set
        :param gen_X_Y: generators of X union Y
        :return: list of frequent sub itemsets
        '''

        fs_star_Y = []

        #Compute Rmin = Minimal({Rk = Sk\X | Sk belongs to Gen_X_Y, Rk included or equal to Z1})
        minimals = RulesAssociationMaximalConstraintMiner.get_minimals(X, Z1, gen_X_Y)
        if len(minimals) == 0: return []

        R_min = minimals

        if len(R_min) == 0: #empty set
            for R_second in Z1:
                fs_star_Y.append(R_second) #includin the empty set
        else:
            R_k_prev = set([])
            R_U_k_prev = set([])
            R_dash_k_prev = Z1

            for k, R_k in enumerate(R_min):
                R_U_k = frozenset(frozenset(R_U_k_prev).union(frozenset(R_k_prev))).difference(R_k)
                R_U_k = list(R_U_k)
                comb_R_U_k = []
                for i in range(len(R_U_k)):
                    comb_R_U_k.extend(combinations(R_U_k, i + 1))
                comb_R_U_k.append(frozenset([]))  # simulate empty element

                for R_k_prime in comb_R_U_k:
                    is_duplicate = False
                    for j in range(k):
                        R_j = R_min[j]
                        if frozenset(R_j).issubset(frozenset(R_k).union(frozenset(R_k_prime))):
                            is_duplicate = True
                            break

                    if not is_duplicate:
                        R_dash_k = frozenset(R_dash_k_prev).difference(frozenset(R_k))
                        R_dash_k = list(R_dash_k)
                        comb_R_dash_k = []
                        for i in range(len(R_dash_k)):
                            comb_R_dash_k.extend(combinations(R_dash_k,i+1))
                        comb_R_dash_k.append(frozenset([]))  # simulate empty element

                        #for R_tild_k in R_dash_k: #for Rmin different from singleton with empty item, we know Rk + R_k_prime + R_tild_k not empty
                        for R_tild_k in comb_R_dash_k: #for Rmin different from singleton with empty item, we know Rk + R_k_prime + R_tild_k not empty
                            fs_star_Y.append(frozenset(R_k).union(frozenset(R_k_prime)).union(frozenset(R_tild_k)))

                #update k variables
                R_U_k_prev = R_U_k
                R_k_prev = R_k
                R_dash_k_prev = R_dash_k

        return fs_star_Y

    def MAR_MaxSC_OneClass(self, L_C1, gen_L_C1, R1, S_star_S1, gen_S_star_S1, S):
        '''
        Generates association rules with the constraints AR*incL1,incR1(L,S) for each pair (L,S) in NFCSincL1,incR1(s0,s1,c0,c1)
        :param L_C1: itemset constraints for rules left side
        :param gen_L_C1: associated generators for L_C1
        :param R1: itemset constraints for rules right side
        :param S_star_S1: closure of considered frequent closed itemsets in LCG(S) to generate rules from
        :param gen_S_star_S1: associated generators for S_star_S1
        :param S: global itemset constraint (L1 union R1)
        :return: associations rules AR*incL1,incR1(L,S)
        '''

        AR_star = []
        FS_star_left = self.MFS_RestrictMaxSC(L_C1,set([]), L_C1,gen_L_C1)
        S_inter_R1 = frozenset(S).intersection(frozenset(R1))
        for L_prime in FS_star_left:
            R1_star = S_inter_R1.difference(L_prime)
            if len(R1_star) > 0: #not empty set
                FS_star_right = self.MFS_RestrictMaxSC(frozenset(S_star_S1).difference(frozenset(L_prime)),L_prime, R1_star, gen_S_star_S1)
                for R_prime in FS_star_right:
                    AR_star.append(RulesAssociationMaximalConstraintMiner.Rule(L_prime,R_prime))

        return AR_star