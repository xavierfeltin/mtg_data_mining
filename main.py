# -*- coding: utf-8 -*-
from loader_magic import MagicLoader, DeckManager
from lsa_encoder import DataCleaner, LSAEncoder
from apriori_analyzer import APrioriAnalyzer
from fpgrowth_analyzer import FPGrowthAnalyzer
from genclose_analyzer import GenCloseAnalyzer as GCA
from genclose_analyzer import RulesAssociationMaximalConstraintMiner as RAMCM
from genclose_analyzer import RuleAssociationMinMin as RAMM
from genclose_analyzer import RuleAssociationMinMax as RAMMax
from itertools import combinations
from tqdm import tqdm

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

    '''
    list_files = os.listdir("./db_decks")  # returns list
    deck_loader.load_from_csv(list_files, card_loader)
    deck_loader.extract_lands(card_loader.lands, card_loader)
    '''

    list_files = os.listdir("./data/decks_mtgdeck_net")  # returns list
    deck_loader.load_from_mtgdeck_csv(list_files, card_loader)
    deck_loader.extract_lands(card_loader.lands, card_loader)

    analyzer = GCA(deck_loader.decks, 0.05)

    print('Start mining ' + str(len(deck_loader.decks)) + ' decks')
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

    rule_miner2 = RAMM(analyzer.lcg_into_list())
    rule_miner = RAMMax(analyzer.lcg_into_list())
    index = 0
    nb_rules = 0
    for pair in combinations(list(range(nb_frequent_items)), 2):
        L = frequent_items[pair[1]]
        S = frequent_items[pair[0]]

        if frozenset(S.closure).issuperset(frozenset(L.closure)):
            #rules = rule_miner.mine(L,S,0.01,0.5,0.8,1.0)
            #rules = rule_miner.mine_cars_L_L(L,0.01,0.5,0.8,1.0)
            rules = []
            RAR = rule_miner.mine_RAR(L, S,0.2,0.5,0.8,1.0)
            rules.extend(RAR)
            rule_miner.mine_CAR2(L, S, RAR, analyzer)

            nb_rules += len(rules)

            for rule in rules:
                left = []
                for item in rule.left:
                    left.append(card_loader.hash_id_name[item])

                right = []
                for item in rule.right:
                    right.append(card_loader.hash_id_name[item])

                print(str(index + 1) + ': ' + ' + '.join([str(item) for item in left]) + ' --> ' + ' + '.join(
                    [str(item) for item in right]) + ', s: ' + str(round(rule.support, 2)) + ', c: ' + str(round(rule.confidence,2)) + ', l: ' + str(round(rule.lift,2)) + ', co: ' + str(round(rule.conviction,2)) + ', rpf: ' + str(round(rule.rpf,2)))

                index += 1

    print('nb rules: ' + str(nb_rules))

def use_reference(file):
    db = []
    with open('./data/'+file+'.dat') as csvfile:
        reader = csvfile.read()
        rows = reader.split('\n')
        for row in rows:
            transaction = row.split(' ')
            db.append(transaction)

    min_support = 0.9
    analyzer = GCA(db, min_support)
    analyzer.mine()
    frequent_items = analyzer.lcg_into_list()
    nb_frequent_items = len(frequent_items)
    print('Nb frequent items with min_support = ' + str(min_support) +': ' + str(nb_frequent_items))

    rule_miner = RAMMax(analyzer.lcg_into_list())
    nb_rules = 0

    print('Extract rules from frequent items: ')
    for pair in tqdm(combinations(list(range(nb_frequent_items)), 2)):
        L = frequent_items[pair[1]]
        S = frequent_items[pair[0]]

        rules = []
        RAR = rule_miner.mine_RAR(L, S, 0.9, 1.0, 0.8, 1.0)
        rules.extend(RAR)
        rules.extend(rule_miner.mine_CAR2(L, S, RAR, analyzer))
        nb_rules += len(rules)

        print('L:' + str(L.closure)+ ', ''S:' + str(S.closure) + ', nb BR min/max: ' + str(len(RAR)) + ', nb CR: ' + str(nb_rules))

    print('nb rules: ' + str(nb_rules))

if __name__ == "__main__":
    # execute only if run as a script
    use_reference('connect')
    #find_closed_items()