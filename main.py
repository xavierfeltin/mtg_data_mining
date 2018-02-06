# -*- coding: utf-8 -*-
from loader_magic import MagicLoader, DeckManager
from lsa_encoder import DataCleaner, LSAEncoder
from apriori_analyzer import APrioriAnalyzer
from fpgrowth_analyzer import FPGrowthAnalyzer
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

if __name__ == "__main__":
    # execute only if run as a script
    #encoding_magic_card
    #find_frequent_items_apriori()
    find_frequent_items_fpgrowth()