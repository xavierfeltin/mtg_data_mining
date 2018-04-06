# -*- coding: utf-8 -*-
from loader_magic import MagicLoader, DeckManager
from lsa_encoder import DataCleaner, LSAEncoder
from apriori_analyzer import APrioriAnalyzer
from fpgrowth_analyzer import FPGrowthAnalyzer
from genclose_analyzer import GenCloseAnalyzer as GCA
from genclose_analyzer import RulesAssociationMaximalConstraintMiner as RAMCM
from genclose_analyzer import RuleAssociationMinMin as RAMM
from itertools import combinations

import os

def encoding_magic_card():
    loader = MagicLoader()
    loader.load('./data/AllCards-x.json')
    cleaner = DataCleaner(loader.texts, loader.names)
    cleaner.clean()
    lsa_transformer = LSAEncoder(cleaner.clean_data)
    lsa_transformer.fit()

def find_frequent_items_apriori():
    card_loader = MagicLoader()
    card_loader.load('./data/AllCards-x.json')

    deck_loader = DeckManager()
    list_files = os.listdir("./db_decks")  # returns list
    deck_loader.load_from_csv(list_files)
    deck_loader.extract_lands(card_loader.lands)

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
    card_loader.load('./data/AllCards-x.json')

    print('Clean deck')
    deck_loader = DeckManager()
    list_files = os.listdir("./db_decks")  # returns list
    deck_loader.load_from_csv(list_files, card_loader)
    deck_loader.extract_lands(card_loader.lands)

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
    card_loader.load('./data/magic_cards/AllCards-x.json')

    print('Clean deck')
    deck_loader = DeckManager()
    list_files = os.listdir("./data/decks_mtgdeck_net")  # returns list
    deck_loader.load_from_mtgdeck_csv(list_files, card_loader)
    deck_loader.extract_lands(card_loader.lands)

    analyzer = GCA(deck_loader.decks, 0.01)

    print('Start mining')
    analyzer.mine()
    print('nb closed items = ' + str(len(analyzer.lcg_into_list())))
    #deck_loader.write_frequent_items_into_csv('genclose_results', analyzer.get_closed_items_closures(), card_loader)

    frequent_items = analyzer.lcg_into_list()
    nb_frequent_items = len(frequent_items)

    generated_rules = []
    '''
    rule_miner = RAMCM(frequent_items)
    for pair in combinations(list(range(nb_frequent_items)), 2):
        L1 = frequent_items[pair[0]].closure
        R1 = frequent_items[pair[1]].closure
        rule_miner.mine(0.3, 1.0, 0.33, 1.0, L1, R1)
        generated_rules.extend(rule_miner.ars)
    '''

    rule_miner = RAMM(frequent_items)
    index = 0
    for pair in combinations(list(range(nb_frequent_items)), 2):
        L = frequent_items[pair[0]]
        S = frequent_items[pair[1]]
        rules = rule_miner.mine(L,S)

        for rule in rules:
            left = []
            for item in rule.left:
                left.append(card_loader.hash_id_name[item])

            right = []
            for item in rule.right:
                right.append(card_loader.hash_id_name[item])

            print(str(index + 1) + ': ' + '+'.join([str(item) for item in left]) + '-->' + '+'.join(
                [str(item) for item in right]))

            index += 1

if __name__ == "__main__":
    # execute only if run as a script
    #encoding_magic_card
    #find_frequent_items_apriori()
    #find_frequent_items_fpgrowth()
    find_closed_items()