import hashlib
from tqdm import tqdm
from collections import OrderedDict
from itertools import combinations, chain
from operator import itemgetter
from math import inf
from time import time
from collections import deque

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

def combination_set(set_to_process, with_empty_set = True, max_len = None):
    '''
    Return all the combinations in a set
    :param set_to_process: set to get all the combinations from
    :param with_empty_set: True to add an empty set to the generation
    :return: yield combinations
    '''
    s = list(set_to_process)
    if max_len is None: max_len = len(s)
    return chain.from_iterable(combinations(s, r) for r in range(1,max_len + 1))

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

            #if transactions is not None:
            #    self.transactions = frozenset(transactions)
            #else:
            #    self.transactions = None

            self.diffset = []
            self.key = 0 #hash key based on sum transactions
            self.folder = None
            self.left_parent = left_parent
            self.right_parent = right_parent

        def get_sum_transaction(self, db_length):
            """
            Return the sum of transactions index for hashing in LCG
            :return: sum
            """
            if self.left_parent is None:
                sum_trans = (db_length*(db_length+1))/2.0
            else:
                sum_trans = self.left_parent.sumO

            for diff in self.diffset:
                sum_trans -= sum(list(diff[1]))

            #return sum(self.transactions)
            return sum_trans

        def to_str(self):
            return '<' + str(self.closure) + ', ' + str(round(self.support,4)) + ', ' + str(self.generators) + '>'

        def add_diffset(self, left_parent, associated_transactions, compute_diffset = True, is_root = False):
            """
            Compute the diffset for the node and the left parent set in argument
            Use essentially for first level of the tree (left_parent will be the root)
            """
            if compute_diffset:
                diffset = self.compute_diffset(left_parent, associated_transactions)
            else:
                diffset = self.compute_diffset(None, associated_transactions)

            if is_root:
                self.diffset.append((None, diffset, self.generators[:]))
            else:
                self.diffset.append((left_parent, diffset, self.generators[:]))

            if left_parent is None:
                self.support = len(diffset)
            else:
                self.support = left_parent.support - len(diffset)

        def compute_diffset(self, left_parent, associated_transactions):
            """
            Compute the diffset between the current node and it left parent
            :param node: current node
            :param left_parent: current node's left parent
            """
            if left_parent is None:
                return associated_transactions
            else:
                all_diff = []
                for diff in left_parent.diffset:
                    all_diff.extend(diff[1])
                #return left_parent.transactions.difference(associated_transactions)
                return frozenset(all_diff).difference(associated_transactions)

    cumulative_time = 0

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

                lp_x_index = -1
                lp_y_index = -1
                for l, LP_X in enumerate(X.diffset):
                    for k, LP_Y in enumerate(Y.diffset):
                        if LP_X[0] == LP_Y[0]:
                            lp_x_index = l
                            lp_y_index = k
                            break
                    if lp_x_index != -1: break

                if lp_x_index != -1:
                    #Left and Right share common left parent
                    # if d(Left,LP) included or equal d(Right,LP) <=> rho(right.H) included or equal rho(left.H)
                    # Case 1: In the case that X.O C Y.O, we extend X.H by Y.H: X.H = X.H union Y.H.
                    is_case_1 = frozenset(X.diffset[lp_x_index][1]) > frozenset(Y.diffset[lp_y_index][1])
                    # Case 2: If X.O includes Y.O, we add X.H to Y.H.
                    is_case_2 = frozenset(X.diffset[lp_x_index][1]) < frozenset(Y.diffset[lp_y_index][1])
                    # Case 3: In the remaining case, this procedure merges Y to X. It pushes all generators in Y.GS to X.GS, adds Y.H to X.H, and discards Y
                    is_case_3 = frozenset(X.diffset[lp_x_index][1]) == frozenset(Y.diffset[lp_y_index][1])
                else:
                    is_case_1 = False
                    is_case_2 = False
                    # Case 3: In the remaining case, this procedure merges Y to X. It pushes all generators in Y.GS to X.GS, adds Y.H to X.H, and discards Y
                    is_case_3 = (X.closure <= Y.closure or  Y.closure <= X.closure) and (X.support == Y.support)


                #if d(Left,LP) included or equal d(Right,LP) <=> rho(right.H) included or equal rho(left.H)
                # Case 1: In the case that X.O C Y.O, we extend X.H by Y.H: X.H = X.H union Y.H.
                if is_case_1:
                    X.closure = X.closure.union(Y.closure)
                    j += 1

                # Case 2: If X.O includes Y.O, we add X.H to Y.H.
                elif is_case_2:
                    Y.closure = Y.closure.union(X.closure)
                    j += 1

                # Case 3: In the remaining case, this procedure merges Y to X. It pushes all generators in Y.GS to X.GS, adds Y.H to X.H, and discards Y
                elif is_case_3:
                    # Recall that we join only i-generators of G1 and G2 ( in the nodes at L[i]),
                    # with common i-1 first items, called the common prefix.
                    i_generators = deque()
                    for generator in Y.generators:
                        if len(generator) == index_level \
                                and (len(frozenset(generator).difference(frozenset(X.i_generator))) == 1):
                            i_generators.append(generator)

                    for Y_diff in Y.diffset:
                        common_left_parent = False
                        for X_diff in X.diffset:
                            if Y_diff[0] == X_diff[0]:
                                X_diff[2].extend(Y_diff[2])
                                common_left_parent = True
                                break
                        if not common_left_parent:
                            X.diffset.append(Y_diff)

                    if len(i_generators) > 0:
                        X.generators.extend(i_generators)
                        X.closure = X.closure.union(Y.closure)

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
                    # do nothing and process next item
                    j += 1

                '''
                Previous verrsion without diffsets        
                frozen_X = X.transactions
                frozen_Y = Y.transactions

                # Case 1: In the case that X.O C Y.O, we extend X.H by Y.H: X.H = X.H union Y.H.
                if frozen_X < frozen_Y:
                    X.closure = X.closure.union(Y.closure)
                    j += 1

                # Case 2: If X.O includes Y.O, we add X.H to Y.H.
                elif frozen_X > frozen_Y:
                    Y.closure = Y.closure.union(X.closure)
                    j += 1

                # Case 3: In the remaining case, this procedure merges Y to X. It pushes all generators in Y.GS to X.GS, adds Y.H to X.H, and discards Y
                elif frozen_X == frozen_Y:
                    #Recall that we join only i-generators of G1 and G2 ( in the nodes at L[i]),
                    # with common i-1 first items, called the common prefix.
                    i_generators = deque()
                    for generator in Y.generators:
                        if len(generator) == index_level \
                            and (len(frozenset(generator).difference(frozenset(X.i_generator))) == 1):
                            i_generators.append(generator)

                    if len(i_generators) > 0:
                        X.generators.extend(i_generators)
                        X.closure = X.closure.union(Y.closure)

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
                '''

    def store_level(self, tree_level):
        """
        Save the closed items in the current tree level inside LCG
        :param tree_level: level to store
        :param lcg: store all the closed items
        """

        for node in tree_level:
            node.sumO = node.get_sum_transaction(self.db_length)
            key = node.sumO
            if key in self.LCG:
                if node.support in self.LCG[key]:
                    existing_closed = self.LCG[key][node.support]
                    not_exist = True
                    for closed in existing_closed:
                        #If there exists itemset P in ℒ CG such that supp(P) = X.Supp and P includes or is equal to X.H,
                        # P is the closure that X.H wants to reach.Thus, the new generators in X.GS are pushed into
                        # the generator list of P and X.H becomes P.
                        if closed.closure.issuperset(node.closure):
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
        key = hashlib.md5(str(key_list).encode('utf-8')).hexdigest()
        return key

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

    def search_node_with_generator(self, generator):
        """
        Return closure containing the generator given in argument
        :param node: left parent
        :param generator: generator to search in closed items in LCG
        :return: node or None if not found
        """

        transactions = []
        for gen in combination_set(generator, max_len=1):
            if len(transactions) == 0:
                transactions = self.get_transactions_with_item(gen[0])
            else:
                transactions = get_list_intersection(transactions, self.get_transactions_with_item(gen[0]))

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
            if search.issubset(closed.closure):
                return closed
        return None

    def mine(self):
        """
        Mine the closed itemsets of the database and the associated generators
        :return: list of nodes <closed itemset, support, generators>
        """

        start_time = time()
        self.clean_database()

        frequent_items = self.sorted_items.keys()
        lcg = deque()
        tree = deque()
        has_new_level = True
        i = 0 # 0 refers to L1

        root = GenCloseAnalyzer.Node(1.0, set(), [])
        root.add_diffset(None,list(range(len(self.database))))

        # Initialiation of layer L1 in the tree
        print('Initialize first layer')
        LCurrent = deque()
        for item in frequent_items:
            associated_transactions = self.get_transactions_with_item(item)
            #LCurrent.append(GenCloseAnalyzer.Node(len(associated_transactions)/self.db_length, item, [item], associated_transactions)) #<support, item, generators, transactions>
            new_node = GenCloseAnalyzer.Node(len(associated_transactions)/self.db_length, item, [item]) #<support, item, generators>
            new_node.add_diffset(root, associated_transactions, is_root = True)
            LCurrent.append(new_node)
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
                        #for right_index, right_node in reverse_enumerate(nodes):
                        for right_index in range(left_index+1,len(nodes)):
                            right_node = nodes[right_index]
                            if left_index < right_index:
                                self.join(left_node, right_node, LNext, i)
                            else:
                                break
            else: #no folder in common for the first level of the tree
                for left_index, left_node in enumerate(LCurrent):
                    #for right_index, right_node in reverse_enumerate(LCurrent):
                    for right_index in range(left_index + 1, len(LCurrent)):
                        right_node = LCurrent[right_index]
                        if left_index < right_index:
                            self.join(left_node, right_node, LNext, i)
                        else:
                            break

            if len(LNext) == 0: has_new_level = False
            LCurrent = LNext
            i += 1

        print('mine time = ' + str((time()-start_time)*1000.0))
        return lcg

    def join(self, left_node, right_node, next_level, current_index):
        """
        utility method to package common code
        """
        ''' Before diffset
        new_transactions = left_node.transactions.intersection(right_node.transactions)
        new_support = len(new_transactions)/self.db_length

        if new_support != left_node.support and new_support != right_node.support and new_support >= self.ratio_min_supp:
            new_closure = left_node.closure.union(right_node.closure)  # using EOA
            self.join_generators(left_node, right_node, new_transactions, new_support, new_closure, next_level, current_index + 1)  # using Condition (5)
        '''

        lp_x_index = -1
        lp_y_index = -1
        for i, LP_X in enumerate(left_node.diffset):
            for j, LP_Y in enumerate(right_node.diffset):
                if LP_X[0] == LP_Y[0]:
                    lp_x_index = i
                    lp_y_index = j
                    break
            if lp_x_index != -1: break

        if lp_x_index != -1:
            new_diffset = right_node.diffset[lp_y_index][1].difference(left_node.diffset[lp_x_index][1])

            new_support = left_node.support - len(new_diffset)
            if new_support != left_node.support and new_support != right_node.support and new_support >= self.ratio_min_supp:
                new_closure = left_node.closure.union(right_node.closure)  # using EOA
                self.join_generators(left_node, right_node, new_diffset, new_support, new_closure, next_level,current_index + 1)  # using Condition (5)

    #def join_generators(self, left_node, right_node, new_transactions, new_support, new_closure, next_level, index_level):
    def join_generators(self, left_node, right_node, new_diffset, new_support, new_closure, next_level, index_level):
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

        left_generators = []
        for left_diff in left_node.diffset:
            for generator in left_diff[2]:
                left_generators.append((left_diff[0], generator))

        right_generators = []
        for right_diff in right_node.diffset:
            for generator in right_diff[2]:
                right_generators.append((right_diff[0], generator))

        new_generators_set = frozenset([])
        for g_left in left_generators:
            for g_right in right_generators:
                if g_left[0] == g_right[0] \
                        and len(g_left[1]) == index_level and len(g_right[1]) == index_level \
                        and len(frozenset(g_left[1]).intersection(frozenset(g_right[1]))) == index_level-1:

                    G = frozenset(g_left[1]).union(frozenset(g_right[1]))
                    G0 = frozenset(g_left[1]).intersection(frozenset(g_right[1]))
                    G_is_generator = True

                    for gen in G0: #combination_set(G0, with_empty_set=False, max_len=len(G0)):
                        Gg = G.difference(gen)
                        node_g = self.search_node_with_generator(Gg)
                        if node_g is None or new_support == node_g.support:
                            G_is_generator = False
                            break #for each G in G0
                        else: #G can be generator
                            new_closure = new_closure.union(node_g.closure) #using EOA

                    if G_is_generator:
                        new_generators_set = new_generators_set.union(G)

        '''
        #Use only generators from diffset with the same left parents
        new_generators_set = []
        lp_x_index = -1
        lp_y_index = -1
        for i, LP_X in enumerate(left_node.diffset):
            for j, LP_Y in enumerate(right_node.diffset):
                if LP_X[0] == LP_Y[0]:
                    lp_x_index = i
                    lp_y_index = j
                    break
            if lp_x_index != -1: break

        #TODO: revoir cette partie avec des frozenset and test if generators have same left parents
        #for left_gen in left_node.generators:
        for left_gen in left_node.diffset[lp_x_index][2]:
            #for right_gen in right_node.generators:
            for right_gen in right_node.diffset[lp_y_index][2]:
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
        '''

        if len(new_generators_set) >= 1:
            #new i+1-generators
            #next_level.append(GenCloseAnalyzer.Node(new_support, new_closure, new_generators_set, new_transactions, left_node, right_node))
            new_node = GenCloseAnalyzer.Node(new_support, new_closure, list(new_generators_set), [], left_node, right_node)
            new_node.add_diffset(left_node, new_diffset, compute_diffset = False) #diffset already computed above
            next_level.append(new_node)

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


class Rule:
    def __init__(self, left, right, support = 1.0, confidence = 1.0, lift = 1.0, conviction = 1.0, rpf = 1.0):
        self.left = left
        self.right = right
        self.support= support
        self.confidence = confidence
        self.lift = lift
        self.conviction = conviction
        self.rpf = rpf

    def to_str(self):
        return '+'.join([str(item) for item in self.left]) + '-->' + '+'.join([str(item) for item in self.right])

class RulesAssociation:
    def __init__(self, lcg):
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
    def combination_set(set_to_process, with_empty_set = True, max_len = None):
        '''
        Return all the combinations in a set
        :param set_to_process: set to get all the combinations from
        :param with_empty_set: True to add an empty set to the generation
        :return: yield combinations
        '''
        s = list(set_to_process)
        return chain.from_iterable(combinations(s, r) for r in range(max_len + 1))

    def mine(self):
        pass

class RulesAssociationMaximalConstraintMiner(RulesAssociation):
    '''
    Rules association miner with configuration on items, support and confidence, based on the following publication:
    - Efficiently mining association rules based on maximum single constraints, Anh Tran, Tin C Truong, Bac Le, 2017
    source: https://link.springer.com/article/10.1007/s40595-017-0096-2
    '''

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

        RulesAssociation.__init__(self, lcg)
        self.s0 = 0
        self.s1 = 1
        self.c0 = 0
        self.c1 = 1
        self.l1 = []
        self.r1 = []

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

        print('MAR_MaxSC(' + str(round(s0,4)) + ', ' + str(round(s1,4)) + ' , ' + str(round(c0,4)) + ', ' + str(round(c1,4)) + ', ' + str(l1) + ', ' + str(r1) + ')')

        self.ars = []
        if s0 > s1 or c0 > c1: return

        S1_star = frozenset(l1).union(frozenset(r1))
        C1 = l1
        supp_C1 = self._get_support(C1)

        #TODO: what is R0? not used after in algorithm...
        #R0_star = R0

        print('\ninitial conditions: ')
        print('s0: ' + str(round(s0, 4)) + ', s1: ' + str(round(s1, 4)) + ', c0: ' + str(round(c0, 4)) + ', c1: ' + str(round(c1, 4)))
        print('L1: ' + str(l1) + ', R1: ' + str(r1))

        s0_star = max(s0, c0 * supp_C1)
        s1_star = s1
        print('s0* = max(s0, c0 x supp(C1)) => ' + str(round(s0_star)))
        print('s1* = s1 => ' + str(round(s1_star)))

        fcs_S1_star = self.MFCS_FromLattice(self.lcg, S1_star, self._get_support(S1_star), s0_star, s1_star) #TODO: from examples looks like S = S1_star ...
        print('FCS⊆S1* = MFCS_FromLattice(LCG, S1*, supp(S1*), s0*, s1*)')
        str_fcs =''
        for item in fcs_S1_star:
            str_fcs += '  - ' + item.to_str() + '\n'
        print('result FCS⊆S1*: \n' + str(str_fcs))

        print('for each <Ss1*, supp(Ss1*), GS1*(S)> ∈ FCS⊆S1*(s0*, s1*) do')
        for S1_closed_item in fcs_S1_star:
            print('  - Ss1*: <'+str(S1_closed_item.closure) +', ' + str(round(S1_closed_item.support,4)) +', '+ str(S1_closed_item.generators) +'>')
            s0_prime = S1_closed_item.support/c1
            s1_prime = min(1, S1_closed_item.support/c0)
            print('s\'0 = supp(Ss1*)/c1 => ' + str(round(s0_prime,4)))
            print('s\'1 = min(1,supp(Ss1*)/c0) => ' + str(round(s1_prime,4)))

            lcg_s = self.MFCS_FromLattice(self.lcg, S1_closed_item.closure, S1_closed_item.support, 0, 1)
            print('LCG_S = MFCS_FromLattice(LCG, S, supp(S), 0, 1)')
            str_lcg_s = ''
            for item in lcg_s:
                str_lcg_s += '  - ' + item.to_str() + '\n'
            print('result LCG_S: \n' + str(str_lcg_s))

            fcs_C1 = self.MFCS_FromLattice(lcg_s, C1, supp_C1, s0_prime, s1_prime)
            print('FCS⊆C1(s\'0,s\'1) = MFCS_FromLattice(LCG_S, C1, supp(S), s\'0, s\'1)')
            str_fcs_C1 = ''
            for item in fcs_C1:
                str_fcs_C1 += '  - ' + item.to_str() + '\n'
            if len(str_fcs_C1) == 0:
                print('result FCS⊆C1(s\'0,s\'1): None')
            else:
                print('result FCS⊆C1(s\'0,s\'1): \n' + str(str_fcs_C1))
                print('for each <LC1, supp(LC1), GC1(L)> ∈ FCS⊆C1(s\'0, s\'1) do')
                for C1_closed_item in fcs_C1:
                    print('  - LC1: <' + str(C1_closed_item.closure) + ', ' + str(round(C1_closed_item.support, 4)) + ', ' + str(C1_closed_item.generators) + '>')
                    print('AR*⊆L1⊆R1(L,S) = MAR_MaxSC_OneClass(LC1,GC1(L),R1,Ss1*,GS1*(S),S)')
                    AR_star = self.MAR_MaxSC_OneClass(C1_closed_item.closure, C1_closed_item.generators, r1,S1_closed_item.closure, S1_closed_item.generators, S1_closed_item.closure)  #TODO: from examples looks like S = S1_star ...
                    str_AR_star = ''
                    for item in AR_star:
                        str_AR_star += '  - ' + item.to_str() + '\n'
                    print('result AR*⊆L1⊆R1(L,S): \n' + str(str_AR_star))
                    self.ars.extend(AR_star)

        str_AR = ''
        for item in self.ars:
            str_AR += '  - ' + item.to_str() + '\n'
        print('\n\n Final result ARS⊆L1⊆R1(s0,s1,c0,c1): \n' + str(str_AR))

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

        #comb_Li = []
        #for i in range(len(C1)):
        #    comb_Li.extend(combinations(C1, i + 1))

        for closed in lcg:
            generators_C1 = []
            if s0 <= closed.support <= s1:
                #if there is Li in G(L) and Li included or equal in C1 then

                for i in range(len(C1)):
                    for li in combinations(C1, i + 1):
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

        print('\ncall MFS_RestrictMaxSC(' + str(set(Y)) + ', ' + str(set(X)) + ' , ' + str(set(Z1)) + ', ' + str(gen_X_Y))

        fs_star_Y = []

        #Compute Rmin = Minimal({Rk = Sk\X | Sk belongs to Gen_X_Y, Rk included or equal to Z1})
        minimals = RulesAssociationMaximalConstraintMiner.get_minimals(X, Z1, gen_X_Y)
        if len(minimals) == 0:
            print('GX+Z1(X+Y) = Ø, return Ø')
            return []

        R_min = minimals

        print('Rmin = Minimal{Rk = Sk\X | Sk ∈ G(X+Y), Rk ⊆ Z1} => ' + str(R_min))

        if len(R_min) == 1 and R_min[0] == frozenset([]): #empty set
            print('if Rmin = {Ø}  => True')
            z1_combination = []
            for i in range(len(Z1)):
                z1_combination.extend(combinations(Z1, i + 1))
            z1_combination.append(frozenset([]))  # simulate empty element

            for R_second in z1_combination:
                fs_star_Y.append(R_second) #including the empty set

            str_fs_star_Y = ''
            for item in fs_star_Y:
                str_fs_star_Y += '  - ' + str(set(item)) + '\n'
            print('result FS*(Y)X⊆Z1*: \n' + str(str_fs_star_Y))

        else:
            print('if Rmin = {Ø}  => False')
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
                            print('  - Add in FS*(Y)X⊆Z1*: Rk('+ str(set(R_k)) + ')' + ', R\'k(' + str(set(R_k_prime)) + '), R~k(' + str(set(R_tild_k)) + ')')

                #update k variables
                R_U_k_prev = R_U_k
                R_k_prev = R_k
                R_dash_k_prev = R_dash_k

                str_fs_star_Y = ''
                for item in fs_star_Y:
                    str_fs_star_Y += '  - ' + str(set(item)) + '\n'
                print('result FS*(Y)X⊆Z1*: \n' + str(str_fs_star_Y))

        print('end call MFS_RestrictMaxSC\n')
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

        print('\ncall MAR_MaxSC_OneClass(' + str(L_C1) +', ' + str(gen_L_C1) +' , ' + str(R1) + ', '+ str(S_star_S1) + ', ' + str(gen_S_star_S1) + ', ' + str(S))

        AR_star = []

        print('FS*⊆LC1 = MFS_RestrictMaxSC(LC1, Ø, LC1, G(LC1))')
        FS_star_left = self.MFS_RestrictMaxSC(L_C1,set([]), L_C1,gen_L_C1)
        str_FS_star_left = ''
        for item in FS_star_left:
            str_FS_star_left += '  - ' + str(set(item)) + '\n'
        print('result FS*⊆LC1: \n' + str(str_FS_star_left))

        print('for each L\' ∈ FS*⊆LC1 and (S∩R1)\L\' != Ø) do')
        S_inter_R1 = frozenset(S).intersection(frozenset(R1))
        for L_prime in FS_star_left:
            R1_star = S_inter_R1.difference(L_prime)
            print('L\': ' + str(set(L_prime)) + ', R1* = (S∩R1)\L\' => ' + str(set(R1_star)))

            if len(R1_star) > 0: #not empty set
                print('FS*(Ss1*\L\')L\'⊆R1* = MFS_RestrictMaxSC(Ss1*\L\', L\', R1*, G(Ss1*))')
                FS_star_right = self.MFS_RestrictMaxSC(frozenset(S_star_S1).difference(frozenset(L_prime)),L_prime, R1_star, gen_S_star_S1)
                str_FS_star_right= ''
                for item in FS_star_right:
                    str_FS_star_right+= '  - ' + str(set(item)) + '\n'
                print('result FS*(Ss1*\L\')L\'⊆R1*: \n' + str(str_FS_star_right))

                for R_prime in FS_star_right:
                    AR_star.append(Rule(L_prime,R_prime))
                    print(' - Add rule ' + Rule(L_prime,R_prime).to_str())

        print('end call MAR_MaxSC_OneClass\n')

        return AR_star

class RuleAssociationMinMin(RulesAssociation):
    '''
    Rules association miner with generation of all basic rules and the consequent rules
    - Structure of Association	Rule Set	Based on MinMin Basic Rules, Anh Tran, Tin C Truong, Thong Trab, 2010
    source: https://www.researchgate.net/publication/261319771
    '''

    def __init__(self, lcg):
        RulesAssociation.__init__(self, lcg)

    @staticmethod
    def get_minimals(Li, S):
        '''
        Return Rmin(L’, S) = {R*ik:=Sk\L’ | Sk∈G(S), Sk\Li is minimal for each Li∈G(L’), R*ik not empty}
        :param Li: one of generator from G(L')
        :param S: list of generators of S
        :return: array of minimals
        '''

        minimals = []
        len_min = inf
        for Sk in S:
            min = frozenset(Sk).difference(frozenset(Li))
            if len(min) <= len_min:
                minimals.append(min)
                len_min = len(min)

        filtered = []
        for min in minimals:
            if len(min) == len_min:
                filtered.append(min)

        return filtered

    def mine_LS(self, L, S, s0, s1, c0, c1):
        '''
        Mine all the basic rules for the frequent itemsets L and S
        :param L: node containing L
        :param S: node containing S
        :param s0: min support
        :param s1: max support
        :param c0: min confidence
        :param c1: max confidence
        :return: all basic rules
        '''
        B_L_S = []

        c = S.support/ L.support
        lift = c / S.support

        if c == 1.0:
            conviction = inf
        else:
            conviction = (1.0 - S.support) / (1.0 - c)

        rule_power_factor = S.support * c

        if c0 <= c <= c1 and s0 <= S.support <= s1:
            for Li in L.generators:
                MS = RuleAssociationMinMin.get_minimals(Li, S.generators)
                for Rk in MS:
                    B_L_S.append(Rule(Li,Rk,S.support,c, lift, conviction, rule_power_factor))
        return B_L_S

    def mine_LL(self, L, s0, s1, c0, c1):
        B_L_L = []

        c = 1.0
        lift = c / L.support
        conviction = inf
        rule_power_factor = L.support

        if c0 <= c <= c1 and s0 <= L.support <= s1:
            if L.closure not in L.generators:
                for L0 in L.generators:
                    a = frozenset(L.closure).difference(frozenset(L0))
                    B_L_L.append(Rule(L0, a, L.support, c))
        return B_L_L

    def mine_cars_L_S(self, L, S, s0, s1, c0, c1, gca):
        B_LS = self.mine_LS(L, S, s0, s1, c0, c1)
        rules = deque()

        if len(B_LS) > 0:
            rules_left_generated = self.left_adding_L_S(L,S, B_LS)
            rules_right_generated = []
            for left_rule in rules_left_generated:
                rules_right_generated.extend(self.right_adding(left_rule.left,S, gca))

            rules.extend(rules_left_generated)
            rules.extend(rules_right_generated)
        return rules

    def mine_cars_L_L(self, L, s0, s1, c0, c1):
        B_LL = self.mine_LL(L, s0, s1, c0, c1)
        rules = deque()

        if len(B_LL) > 0:
            rules_left_generated = self.left_adding_L_L(L, B_LL)
            rules_right_generated = []
            for left_rule in rules_left_generated:
                rules_right_generated.extend(self.right_adding(left_rule.left, S))

            rules.extend(rules_left_generated)
            rules.extend(rules_right_generated)

        return rules

    def right_adding(self, L_prime, S, gca):
        node_lprime = gca.search_node_with_closure(L_prime)
        right_generated_rules = []
        MS = RuleAssociationMinMin.get_minimals(L_prime, S.generators)
        S_U_Lprime = set()
        for Ri in MS:
            S_U_Lprime = S_U_Lprime.union(set(Ri))

        K_U_Lprime = set()
        for Li in node_lprime.generators:
            K_U_Lprime = K_U_Lprime.union(set(Li))

        S_tild_L = S.closure.difference(K_U_Lprime.union(node_lprime.closure))

        for R_tild in RulesAssociation.combination_set(S_tild_L, False):
            for i, Ri in enumerate(MS):
                S_U_Lprime_i = S_U_Lprime.difference(Ri)
                for Riprime in S_U_Lprime_i:
                    if len(frozenset([Riprime])) > 0 or len(R_tild) > 0:
                        repeated = False
                        if i > 0:
                            for k in range(i):
                                Rk = MS[k]
                                if Rk.issubset(Ri.union(frozenset([Riprime]))):
                                    repeated = True
                                    break #for each Rk
                        if not repeated:
                            right_generated_rules.append(Rule(L_prime,Ri.union(frozenset([Riprime])).union(frozenset(R_tild))))
        return right_generated_rules

    def left_adding_L_S(self, L, S, B_LS):

        left_generated_rules = []
        FS1_L_S = deque()
        Ku = set()
        for Li in L.generators:
            Ku = Ku.union(set(Li))

        right_rules_processed = deque()
        for rule in B_LS:
            if rule.right not in right_rules_processed:
                right_rules_processed.append(rule.right)
                for i, Li in enumerate(L.generators):
                    set_Li = frozenset(Li)
                    Rstar = RuleAssociationMinMin.get_minimals(Li, S.generators)
                    FS_Li_Rstar = self._build_FS_(Li, Rstar, L, Ku)
                    K_U_Li = Ku.difference(set_Li)

                    for Li_Ltild in FS_Li_Rstar:
                        for Lprime_i in RulesAssociation.combination_set(K_U_Li,False):
                            set_Lprime_i = frozenset(Lprime_i)
                            repeated = False
                            if i > 0:
                                for k in range(i):
                                    Lk = L.generators[k]
                                    if frozenset(Lk).issubset(set_Li.union(set_Lprime_i).difference(frozenset(Rstar))):
                                        repeated = True
                                        break #for each Lk
                            if not repeated:
                                left_generated_rules.append(Rule(Li_Ltild.union(set_Lprime_i).difference(Li), rule.right, rule.support, rule.confidence))

        return left_generated_rules

    def left_adding_L_L(self, L, B_LL):

        left_generated_rules = []
        FS1_L_S = deque()
        FS2_L_S = deque()
        Ku = set()
        for Li in L.generators:
            Ku = Ku.union(set(Li))

        for i, Li in enumerate(L.generators):
            set_Li = frozenset(Li)
            K_U_Li = Ku.difference(set_Li)

            for Lstar in self.combination_set(L.closure.difference(Li)):
                set_Lstar = frozenset(Lstar)
                FS_Li_Lstar = self._build_FS_(set_Li, Lstar, L, Ku)
                for Li_Ltild in FS_Li_Lstar:
                    if len(Li_Ltild) > 1 and len(Lstar) >= 1:
                        for Lprime_i in K_U_Li:
                            set_Lprime_i = frozenset([Lprime_i])
                            repeated = False
                            if i > 0:
                                for k in range(i):
                                    Lk = L.generators[k]
                                    if Lk.subset(set_Li.union(set_Lprime_i).difference(set_Lstar)):
                                        repeated = True
                                        break  # for each Li
                            if not repeated:
                                FS2_L_S.append(Li_Ltild.union(set_Lprime_i))

            for Lprime in FS2_L_S:
                for rule in B_LL:
                    left_generated_rules.append(Rule(Lprime, rule.right, rule.support, rule.confidence))

        return left_generated_rules

    def _build_FS_(self, Li, Star, L, Ku):
        '''
        FS_(Li, R) = {Li+L~ | L~⊆K~R}
        :param Li: Li
        :param Star: R* or L*
        :param L: Node L
        :param Ku: Ku computed outside since common to all Li
        :return: FS_(Li,Star)
        '''
        K_tild_R = L.closure.difference(Ku.union(Star))

        FS_ = deque()
        for Ltild in RulesAssociation.combination_set(K_tild_R, False):
            FS_.append(frozenset(Li).union(frozenset(Ltild)))

        return FS_

class RuleAssociationMinMax(RulesAssociation):
    def __init__(self, lcg):
        RulesAssociation.__init__(self, lcg)


    def mine_RAR(self, L, S, s0, s1, c0, c1, ):
        '''
        RAR(L, S) ≡ {r0: GenL→S\GenL | GenL∈Gen(L)}
        :return: RAR(L, S)
        '''

        rules = deque()
        s_rule = S.support
        c_rule = S.support/ L.support

        if s0 <= s_rule <= s1 and c0 <= c_rule <= 1:
            for gen_L in L.generators:
                rules.append(Rule(frozenset(gen_L), S.closure.difference(frozenset(gen_L)), s_rule, c_rule))
        return rules

    def mine_CAR(self, L, S, RAR, gca):
        rules = []
        rd_rules = self.mine_Rd(S, RAR, gca)
        rm_RAR_rules = self.mine_Rm(L, S, RAR, gca)
        rm_Rd_rules = self.mine_Rm(L, S, rd_rules, gca)
        rules.extend(rd_rules)
        rules.extend(rm_RAR_rules)
        rules.extend(rm_Rd_rules)
        return rules

    def mine_CAR2(self, L, S, RAR, gca):
        CAR = []
        Rd_AR = []
        Rm_AR = []

        '''
        N = []
        processed = []
        for gen_S in S.generators:
            S_GenS = S.closure.difference(frozenset(gen_S))
            if S_GenS not in processed:
                processed.append(S_GenS)
                for combination in RulesAssociation.combination_set(S_GenS, False):
                    if frozenset(combination) not in N:
                        N.append(frozenset(combination))
        '''

        for i, rule in enumerate(RAR):
            Rm_AR.extend(self.MA(rule.left, rule.right, L, S, i, rule.support, rule.confidence))
            if rule.confidence == 1:
                for R in self.combination_set(rule.right,False,len(rule.right)-1):
                    print(Rule(rule.left, R, rule.support, 1).to_str())
                    #Rd_AR.append(Rule(rule.left, R, rule.support, 1))
                    Rm_AR.extend(self.MA(rule.left, frozenset(R), L, S, i, rule.support, 1))
            else:
                for R in self.combination_set(rule.right, False, len(rule.right) - 1):
                    node_SR = gca.search_node_with_closure(S.closure.difference(frozenset(R)))
                    if node_SR.closure == S.closure:
                        #Rd_AR.append(Rule(rule.left, rule.right.difference(R), rule.support, rule.confidence))
                        print(Rule(rule.left, R, rule.support, 1).to_str())
                        Rm_AR.extend(self.MA(rule.left, rule.right.difference(R), L, S, i, rule.support, rule.confidence))

        CAR.extend(Rd_AR)
        CAR.extend(Rm_AR)
        return CAR

    def mine_Rd(self, S, RAR, gca):
        '''
        ∀r:L→R ∈ AR: Rd(r) = {s:L→R\R’ | ∅⊂R’⊂R, R’∈N(L+R)}
        N(S) = {A: ∅ ≠ A ⊆ S\GenS, GenS∈ Gen(S)}
        :return: Rd(r)
        '''

        rules = []
        for rule in RAR:
            L = rule.left
            R = rule.right
            N = []
            processed = []
            for gen_S in S.generators:
                S_GenS = S.closure.difference(frozenset(gen_S))
                if S_GenS not in processed:
                    processed.append(S_GenS)
                    for combination in RulesAssociation.combination_set(S_GenS, False):
                        if frozenset(combination) not in N:
                            N.append(frozenset(combination))

            for Rprime in N:
                if Rprime.issubset(R):
                    rules.append(Rule(rule.left, rule.right.difference(Rprime)))

        return rules

    def MA(self, Li, R, L, S, i, support, confidence):
        rules = []
        #node_LiR = gca.search_node_with_closure(frozenset(Li).union(R))
        #if node_LiR.closure == S.closure:
        R_inter_L = R.intersection(L.closure)
        if len(R_inter_L) > 0:
            for Rprime in self.combination_set(R_inter_L, False):
                if set(Rprime) != R:
                    if i == 0:
                        #rules.append(Rule(frozenset(Li).union(frozenset(Rprime)), R.difference(frozenset(Rprime)), support, confidence))
                        print(Rule(frozenset(Li).union(frozenset(Rprime)), R.difference(frozenset(Rprime)), support, confidence).to_str())
                    else:
                        for k in range(i):
                            if not frozenset(L.generators[k]).issubset(frozenset(Li).union(frozenset(Rprime))):
                                #rules.append(Rule(frozenset(Li).union(frozenset(Rprime)),R.difference(frozenset(Rprime)), support, confidence))
                                print(Rule(frozenset(Li).union(frozenset(Rprime)),R.difference(frozenset(Rprime)), support, confidence).to_str())

        return rules

    def mine_Rm(self, L, S, RAR, gca):
        '''
        Sm(L, S) ≡ {ri:Li+R’→ R\R’ | h(Li+R)=S, Li∈Gen(L), ∅≠R’⊆R∩L, R’≠R,
        (i=1 or (i>1 and ∀k: 1≤ k <i: Lk⊄Li+R’))}
        :return: Sm(L, S)
        '''

        rules = []
        for rule in RAR:
            #L = rule.left
            R = rule.right
            #node_L = gca.search_node_with_closure(L)
            #for i, Li in enumerate(node_L.generators):
            for i, Li in enumerate(L.generators):
                node_LiR = gca.search_node_with_closure(frozenset(Li).union(R))
                if node_LiR.closure == S.closure:
                    R_inter_L = R.intersection(L.closure)
                    if len(R_inter_L) > 0:
                        for Rprime in self.combination_set(R_inter_L, False):
                            if set(Rprime) != R:
                                if i == 0:
                                    rules.append(Rule(frozenset(Li).union(frozenset(Rprime)), R.difference(frozenset(Rprime))))
                                else:
                                    for k in range(i):
                                        if not frozenset(L.generators[k]).issubset(frozenset(Li).union(frozenset(Rprime))):
                                            rules.append(Rule(frozenset(Li).union(frozenset(Rprime)),R.difference(frozenset(Rprime))))
        return rules