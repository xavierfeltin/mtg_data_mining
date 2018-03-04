import hashlib
from collections import OrderedDict
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
        def __init__(self, support, closure, generators, transactions, left_parent=None):
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

        def get_sum_transaction(self):
            """
            Return the sum of transactions index for hashing in LCG
            :return: sum
            """
            return sum(self.transactions)

    def __init__(self, database, min_support = 1.0):
        self.database = database
        self.ratio_min_supp = min_support
        self.min_supp = round(len(self.database) * self.ratio_min_supp)
        self.sorted_items = None
        self.reverse_db = {} #fast access to transactions containing a particular item
        self.L_folders = {} #folders regrouping nodes with common prefixes
        #self.LCG = {} #double hash store (transaction sum + support)
        #TODO: implement double hash with diffset
        self.LCG = [] #double hash store (transaction sum + support)

    def lcg_into_list(self):
        """
        Return LCG as a list
        :return: list of all closed itemsets and their generators
        """
        list_closed = []
        for key_sum in self.LCG.keys():
            for key_supp, closed_list in self.LCG[key_sum].items():
                list_closed.extend(closed_list)
        return list_closed

    def clean_database(self):
        """
        Return a list of items with a support greater than min_support
        :return: list of items
        """
        items = {}
        database_size = 0

        # Scan the database to initialize the frequence of all items used in the transactions
        for index, transaction in enumerate(self.database):
            for item in transaction:
                if item in items:
                    items[item] += 1
                    self.reverse_db[item].append(index)
                else:
                    items[item] = 1
                    self.reverse_db[item] = [index]

                database_size += 1

        # Sort the items by increasing frequencies and renumerate the items (most frequent items = biggest number)
        # Skip the items with a frequency lower than the support
        self.sorted_items = sorted(items.items(), key=lambda x: x[1] >= self.min_supp)
        self.sorted_items = OrderedDict(sorted(items.items(), key=itemgetter(1, 0), reverse=False))

        # Reduce the database size by ignoring non frequent items and empty transactions
        transactions = []
        for transaction in self.database:
            list_items = []
            for item in transaction:
                if item in self.sorted_items:
                    list_items.append(item)
            transactions.append(transaction)
        self.database = transactions

    def get_transactions_with_item(self, item):
        """
        Return a list of transactions containing the item
        :return: list of transactions
        """
        return self.reverse_db[item]

    def extend_merge(self, tree_level, index_level):
        """
        Complete the closure of the nodes in the tree_level in parameters (operator EOB)
        :param tree_level: slice of the tree containing the nodes to complete
        :param index_level: current level index in the referential 1..N (and not 0..N-1)
        """
        for i in range(len(tree_level)-1):
            j = i+1
            while j < len(tree_level):
                X = tree_level[i]
                Y = tree_level[j]

                # Case 1: In the case that X.O C Y.O, we extend X.H by Y.H: X.H = X.H union Y.H.
                if frozenset(X.transactions) < (frozenset(Y.transactions)):
                    X.closure = frozenset(X.closure).union(frozenset(Y.closure))
                    j += 1

                # Case 2: If X.O includes Y.O, we add X.H to Y.H.
                elif frozenset(X.transactions) > (frozenset(Y.transactions)):
                    Y.closure = frozenset(Y.closure).union(frozenset(X.closure))
                    j += 1

                # Case 3: In the remaining case, this procedure merges Y to X. It pushes all generators in Y.GS to X.GS, adds Y.H to X.H, and discards Y
                elif frozenset(X.transactions) == (frozenset(Y.transactions)):
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

                        # Hence, if Y is not in the same folder with X, we move all nodes that are in the folder containing
                        # Y to the folder containing X. Thus, X also has the prefixes of Y.
                        if GenCloseAnalyzer.key_folder(Y.folder) != GenCloseAnalyzer.key_folder(X.folder):
                            folder_to_delete = Y.folder
                            for node in self.L_folders[GenCloseAnalyzer.key_folder(Y.folder)]:
                                node.folder = X.folder
                                self.L_folders[GenCloseAnalyzer.key_folder(X.folder)].append(node)
                            del self.L_folders[GenCloseAnalyzer.key_folder(folder_to_delete)]

                        self.L_folders[GenCloseAnalyzer.key_folder(Y.folder)].remove(Y)
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
        '''
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
                        self.LCG[key][node.support] = [GenCloseAnalyzer.Node(node.support, node.closure, node.generators, None)]
                else:
                    self.LCG[key][node.support] = [GenCloseAnalyzer.Node(node.support, node.closure, node.generators, None)]
            else:
                self.LCG[key] = {}
                self.LCG[key][node.support] = [GenCloseAnalyzer.Node(node.support, node.closure,node.generators, None)]
        '''
        #TODO: implement double hash with diffset
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

        '''
        key_sum = node.left_parent.get_sum_transaction()
        if key_sum in self.LCG:
            if node.support in self.LCG[key_sum]:
                for closed in self.LCG[key_sum][node.support]:
                    for gen in closed.generators:
                        if frozenset(gen) == frozenset(generator):
                            return closed
        return None
        '''

        #TODO: implement double hash with diffset
        for closed in self.LCG:
            for gen in closed.generators:
                if frozenset(gen) == frozenset(generator):
                    return closed
        return None

    def search_node_with_closure(self, search):
        # TODO: implement double hash with diffset
        for closed in self.LCG:
            if frozenset(search) == frozenset(closed.closure):
                return closed
        return None

    def mine(self):
        """
        Mine the closed itemsets of the database and the associated generators
        :return: list of nodes <closed itemset, support, generators>
        """
        self.clean_database()
        frequent_items = self.sorted_items.keys()
        lcg = []
        tree = []
        has_new_level = True
        i = 0 # 0 refers to L1

        # Initialiation of layer L1 in the tree
        L1 = []
        for item in frequent_items:
            associated_transactions = self.get_transactions_with_item(item)
            L1.append(GenCloseAnalyzer.Node(len(associated_transactions), item, [item], associated_transactions)) #<support, item, generators, transactions>
        tree.append(L1)

        # Mine the itemsets and generators
        while has_new_level:
            self.attribute_folders(tree[i],i+1) #dispatch items into folders
            self.extend_merge(tree[i],i+1) #using EOB (complete function of the nodes of the same level
            self.store_level(tree[i]) #store the closed itemsets and generators inside LCG

            tree.append([]) #produce (i+1)-generators abd extend corresponding pre-closed itemsets by EOC
            #TODO: improve to filter only by folders to avoid uninteresting pair testing ...
            for left_index, left_node in enumerate(tree[i]):
                for right_index, right_node in reverse_enumerate(tree[i]):
                    if left_index < right_index and (i == 0 or left_node.folder == right_node.folder):
                        new_transactions = frozenset(left_node.transactions).intersection(frozenset(right_node.transactions))
                        new_support = len(new_transactions)

                        if new_support != left_node.support and new_support != right_node.support and new_support >= self.min_supp:
                            new_closure = frozenset(left_node.closure).union(frozenset(right_node.closure)) #using EOA
                            self.join_generators(left_node, right_node, new_transactions, new_support, new_closure, tree[i+1],i+1) #using Condition (5)
                    elif left_index >= right_index:
                        break
            if len(tree[i+1]) == 0: has_new_level = False
            i += 1
        return lcg

    def join_generators(self, left_node, right_node, new_transactions, new_support, new_closure, tree_next_level, index_level):
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
            tree_next_level.append(GenCloseAnalyzer.Node(new_support, new_closure, new_generators_set, new_transactions, left_node))