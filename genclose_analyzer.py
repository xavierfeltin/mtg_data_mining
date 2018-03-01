from collections import OrderedDict
from operator import itemgetter

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
        def __init__(self, support, closure, generators, transactions):
            self.support = support
            self.closure = closure
            self.generators = generators
            self.transactions = transactions
            self.diffset = []
            self.key = 0 #hash key based on sum transactions

    def __init__(self, database, min_support = 1.0):
        self.db = database
        self.ratio_min_supp = min_support
        self.min_supp = len(self.db) * self.ratio_min_supp
        self.sorted_items = None
        self.reverse_db = None

    def clean_database(self):
        """
        Return a list of items with a support greater than min_support
        :return: list of items
        """

        self.reverse_db = {}

        # Scan the database to initialize the frequence of all items used in the transactions
        for index, transaction in enumerate(self.database):
            for item in transaction:
                if item in self.items:
                    self.items[item] += 1
                    self.reverse_db[item].append(index)
                else:
                    self.items[item] = 1
                    self.reverse_db[item] = []

                self.database_size += 1

        # Sort the items by increasing frequencies and renumerate the items (most frequent items = biggest number)
        # Skip the items with a frequency lower than the support
        self.sorted_items = sorted(self.items.items(), key=lambda x: x[1] >= self.min_supp)
        self.sorted_items = OrderedDict(sorted(self.items.items(), key=itemgetter(1, 0), reverse=False))

        # Reduce the database size by ignoring non frequent items and empty transactions
        transactions = []
        for transaction in self.database:
            list_items = []
            for item in transaction:
                if item in self.items:
                    list_items.append(item)
            transactions.append(transaction)
        self.db = transactions

    def get_transactions_with_item(self, item):
        """
        Return a list of transactions containing the item
        :return: list of transactions
        """
        return self.reverse_db[item]

    def extend_merge(self, tree_level):
        """
        :param tree_level:
        :return:
        """
        pass

    def store_level(self, tree_level, lcg):
        """
        :param tree_level:
        :param lcg:
        :return:
        """
        pass

    def is_same_folder(self, left_node, right_node):
        """

        :param left_node:
        :param right_node:
        :return:
        """
        pass

    def compute_diffset(self, node, left_parent):
        """
        Compute the diffset for the node and the left parent set in argument
        diffset =
        """
        diffset = frozenset(left_parent.transactions).difference(frozenset(node.transactions))
        node.support = left_parent.support - len(diffset)
        node.diffset.append(left_parent, diffset, node.generators)

        return diffset,

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
            self.extend_merge(tree[i]) #using EOB (complete function of the nodes of the same level
            self.store_level(tree[i], lcg) #store the closed itemsets and generators inside LCG

            tree.append([]) #produce (i+1)-generators abd extend corresponding pre-closed itemsets by EOC
            for left_index, left_node in enumerate(tree[i]):
                for right_index, right_node in reversed(enumerate(tree[i])):
                    if left_index < right_index and self.is_same_folder(left_index, right_index):
                        new_transactions = frozenset(left_node.transactions).intersection(frozenset(right_node.transactions))
                        new_support = len(new_transactions)

                        if new_support != left_node.support and new_support != right_node.support and new_support >= self.min_supp:
                            new_closure = frozenset(left_node.closure).union(frozenset(right_node.closure)) #using EOA
                            self.join_generators(left_node, right_node, new_transactions, new_support, new_closure, tree[i+1]) #using Condition (5)
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
        :param index_level: current tree level processed
        :return: None
        """

        new_generators_set = set()

        for left_gen in left_node.generators:
            for right_gen in right_node.generators:
                if len(left_gen) == index_level \
                        and len(right_gen) == index_level \
                        and len(frozenset(left_gen).intersection(frozenset(right_gen))) == (index_level-1):
                    generator_candidate = frozenset(left_gen).union(frozenset(right_gen))
                    common_generators = frozenset(left_gen).intersection(frozenset(right_gen))
                    candidate_is_generator = True

                    for gen in common_generators:
                        subset_gen = generator_candidate.remove(gen)
                        matching_node = self.search_node_with_generator(subset_gen)
                        if matching_node is None or new_support == matching_node.support:
                            candidate_is_generator = False
                            break #for each gen in common_generators
                        else:
                            #generator_candidate can be a generator
                            new_closure = frozenset(new_closure).union(frozenset(matching_node.closure)) #using EOA

                    if candidate_is_generator:
                        new_generators_set = frozenset(new_generators_set).union(generator_candidate)

        if len(new_generators_set) >= 1:
            #new i+1-generators
            tree_next_level.append(GenCloseAnalyzer.Node(new_support, new_closure, new_generators_set, new_transactions))




