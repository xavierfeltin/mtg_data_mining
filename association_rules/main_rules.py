# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#

from loader.deck_manager import MagicLoader, DeckManager
from lsa.lsa_encoder import DataCleaner, LSAEncoder
from association_rules.apriori_analyzer import APrioriAnalyzer
from association_rules.fpgrowth_analyzer import FPGrowthAnalyzer
from association_rules.genclose_analyzer import GenCloseAnalyzer as GCA
from association_rules.genclose_analyzer import RuleAssociationMinMax as RAMMax
from collections import deque

import os

def encoding_magic_card():
    loader = MagicLoader()
    loader.load('./../data/AllCards-x.json')
    cleaner = DataCleaner(loader.texts, loader.names)
    cleaner.clean()
    lsa_transformer = LSAEncoder(cleaner.clean_data)
    lsa_transformer.fit()

def find_frequent_items_apriori():
    card_loader = MagicLoader()
    card_loader.load('./../data/AllCards-x.json')

    list_files = os.listdir("./../data/decks_mtgdeck_net")
    for i in range(len(list_files)): # returns list
        list_files[i] = './../data/decks_mtgdeck_net/' + list_files[i]
    deck_loader = DeckManager()
    deck_loader.load_from_mtgdeck_csv(list_files, card_loader)

    print('Data loaded, creating cache')
    analyzer = APrioriAnalyzer(deck_loader.decks[0:10])
    cache_count = APrioriAnalyzer.load_cache_count()
    if cache_count is None:
        cache_count = analyzer.create_cache_count(analyzer.dataset)

    print('Cache created or loaded, start Apriori')
    L, support_data = analyzer.apriori(analyzer.dataset[0:10], minsupport=0.5, cache_count=cache_count)

    print('Apriori done, rules generating')
    rules = analyzer.generateRules(L, support_data, min_confidence=0.9)

    print('Rules generation done')
    analyzer.export_rules('generated_rules', rules)


def find_frequent_items_fpgrowth():
    print('Load deck')
    card_loader = MagicLoader()
    card_loader.load('./../data/AllCards-x.json')

    print('Clean deck')
    list_files = os.listdir("./../data/decks_mtgdeck_net")
    for i in range(len(list_files)):  # returns list
        list_files[i] = './../data/decks_mtgdeck_net/' + list_files[i]
    deck_loader = DeckManager()
    deck_loader.load_from_mtgdeck_csv(list_files, card_loader)

    cards_usage = APrioriAnalyzer.load_cache_count()
    deck_loader.extract_high_used_cards(cards_usage, len(deck_loader.decks)*0.01)

    print('Prepare deck for FPGrowth')
    minSupport = len(deck_loader.decks)*0.001
    initSet = FPGrowthAnalyzer.createInitSet(deck_loader.decks)

    print('Create FPGrowth tree')
    myFPtree, myHeaderTab = FPGrowthAnalyzer.createTree(initSet, minSupport)
    freqItems = []

    print('Mine FPGrowth tree')
    FPGrowthAnalyzer.mineTree(myFPtree, myHeaderTab, minSupport, set([]), freqItems)
    FPGrowthAnalyzer.export_frequent_items('generated_freq_items', freqItems)

    print('Convert frequent sets for generating rules')
    L_hash = {}
    for item in freqItems:
        if len(item) in L_hash:
            L_hash[len(item)].append(item)
        else:
            L_hash[len(item)] = []

    L = []
    for i in sorted(L_hash.keys()):
        L.append(map(frozenset,L_hash[i]))

    analyzer = APrioriAnalyzer(deck_loader.decks)
    _, support_data = analyzer.scanD(analyzer.data_into_set, map(frozenset, freqItems), minSupport)

    print('Generating rules')
    rules = analyzer.generateRules(L, support_data, min_confidence=0.7)

    print('Writing rules')
    analyzer.export_rules('generated_rules', rules)

def find_closed_items():
    print('Load deck')
    card_loader = MagicLoader()
    card_loader.load('./../data/magic_cards/AllCards-x.json')

    print('Clean deck')
    deck_loader = DeckManager()

    list_files = os.listdir("./../data/decks_mtgdeck_net")
    for i in range(len(list_files)): # returns list
        list_files[i] = './../data/decks_mtgdeck_net/' + list_files[i]

    deck_loader.load_from_mtgdeck_csv(list_files, card_loader)
    deck_loader.extract_lands(card_loader.lands, card_loader)

    analyzer = GCA(deck_loader.decks, 0.05)

    print('Start mining ' + str(len(deck_loader.decks)) + ' decks')
    analyzer.mine()
    print('nb closed items = ' + str(len(analyzer.lcg_into_list())))
    #deck_loader.write_frequent_items_into_csv('genclose_results', analyzer.get_closed_items_closures(), card_loader)

    frequent_items = analyzer.lcg_into_list()
    lattice = analyzer.lcg_into_lattice()

    generated_rules = []
    '''
    rule_miner = RAMCM(frequent_items)
    for pair in combinations(list(range(nb_frequent_items)), 2):
        L1 = frequent_items[pair[0]].closure
        R1 = frequent_items[pair[1]].closure
        rule_miner.mine(0.3, 1.0, 0.33, 1.0, L1, R1)
        generated_rules.extend(rule_miner.ars)
    '''

    rule_miner = RAMMax(analyzer.lcg_into_list())


    nb_rules = 0
    nb_basic_rules = 0
    print('Extract rules from frequent items: ')

    for node in lattice.values():
        S = node.fci
        #print('S: ' + str(S.closure))

        to_extract = deque()
        to_extract.append(node)
        to_extract.extend(node.children)
        visited = deque()
        while len(to_extract) > 0:
            current = to_extract.popleft()
            visited.append(current)
            L = current.fci

            RAR = rule_miner.mine_RAR(L, S, 0.05, 0.08, 0.7, 0.9)
            '''
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
            '''

            for rule in RAR:
                text = str(round(rule.support,2)) + ' - ' + str(round(rule.confidence, 2)) + ': '
                for l in rule.left:
                    text += card_loader.hash_id_name[l] + ' + '
                text += ' ----> '
                for r in rule.right:
                    text += card_loader.hash_id_name[r] +  ' + '
                print(text)

    print('nb rules: ' + str(nb_rules))

def use_reference(file):
    db = []
    with open('./../data/'+file+'.dat') as csvfile:
        reader = csvfile.read()
        rows = reader.split('\n')
        for row in rows:
            transaction = row.split(' ')
            db.append(transaction)

    min_support = 0.95
    analyzer = GCA(db, min_support)
    analyzer.mine()
    frequent_items = analyzer.lcg_into_list()

    lattice = analyzer.lcg_into_lattice()

    nb_frequent_items = len(frequent_items)
    print('Nb frequent items with min_support = ' + str(min_support) +': ' + str(nb_frequent_items))

    rule_miner = RAMMax(analyzer.lcg_into_list())
    #rule_miner = RAMin(analyzer.lcg_into_list())

    nb_rules = 0
    nb_basic_rules = 0
    print('Extract rules from frequent items: ')

    rules = deque()
    for node in lattice.values():
        S = node.fci
        print('S: ' + str(S.closure))

        to_extract = deque()
        to_extract.append(node)
        visited = deque()
        while len(to_extract) > 0:
            current = to_extract.popleft()
            visited.append(current)
            L = current.fci

            #RAR = rule_miner.mine_basic(L, S)
            RAR = rule_miner.mine_RAR(L, S, 0.95, 1.0, 0.95, 1.0)
            ne_rules = rule_miner.mine_CAR2(L, S, RAR, analyzer)

            is_new_rule = True
            for new_rule in ne_rules :
                for saved_rules in rules:
                    if new_rule.left == saved_rules.left and new_rule.right == saved_rules.right:
                        is_new_rule = False
                        break
                if is_new_rule:
                    rules.append(new_rule)
                    nb_rules += 1


            #nb_basic_rules += len(RAR)

            print('  - L:' + str(L.closure) + ',gen: ' + str(L.generators) + ', nb BR min/max: ' + str(len(RAR)) + ', TBR: ' + str(nb_basic_rules) +', TBC: ' + str(nb_rules))
            #print(' - L:' + str(L.closure) + ',gen: ' + str(L.generators) + ', nb BR min/max: ' + str(len(RAR)) + ', TBR: ' + str(nb_basic_rules))
            for rule in RAR:
                print('  - ' + rule.to_str())

            for child in current.children:
                for grandchild in child.children:
                    if grandchild not in to_extract and grandchild not in visited:
                        to_extract.append(grandchild)

    print('nb rules: ' + str(nb_basic_rules))

if __name__ == "__main__":
    # execute only if run as a script
    #use_reference('connect')
    find_closed_items()