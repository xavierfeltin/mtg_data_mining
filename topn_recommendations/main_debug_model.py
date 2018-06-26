# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Main for building and saving models
#

import os

from loader.magic_loader import MagicLoader
from loader.deck_manager import DeckManager
from collaborative_filtering.item_to_item import ItemToItem
from topn_recommendations.models.bpr_knn import BPRKNN
from random import randint

def load_magic_environment():
    print('Load magic environment')
    card_loader = MagicLoader()
    card_loader.load_from_set('./../data/magic_cards/AllSets-x.json')
    return card_loader

def load_decks(card_loader):
    print('Load decks')

    files = os.listdir("./../data/decks_mtgdeck_net_extended")  # returns list
    paths = []
    for file in files:
        paths.append('./../data/decks_mtgdeck_net_extended/' + file)

    decks = {}
    for mode in MagicLoader.HASH_GAME_STRING_CODE.keys():
        for path in paths:
            if mode.lower() in path:
                deck_loader = DeckManager()
                deck_loader.load_from_mtgdeck_csv([path], cards_loader=card_loader, ignore_land=True)
                deck_loader.sort_decks()
                decks[mode] = deck_loader

    return decks

def get_cards_from_decks(decks_loader, card_loader):
    multiverseid_in_decks = set()
    for mode in decks_loader:
        multiverseid_in_decks = multiverseid_in_decks.union(decks_loader[mode].cards)
    list_multiverseid_in_decks = list(multiverseid_in_decks)
    cards_in_decks = card_loader.extract_cards(list_multiverseid_in_decks)
    return cards_in_decks

def prepare_deck_data(decks_loader, mode, color, nb_runs):
    decks_to_prepare = decks_loader[mode].grouped_decks[color]
    runs_random_items = []
    for i in range(nb_runs):
        random_items = []
        for deck in decks_to_prepare:
            index = randint(0, len(deck) - 1)
            random_items.append(deck[index])

        for j, card in enumerate(random_items):
            decks_to_prepare[j].remove(card)

        runs_random_items.append(random_items)

    return decks_to_prepare, runs_random_items

if __name__ == "__main__":
    print('Load Magic environment')
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)

    studied_decks = {}
    studied_decks[MagicLoader.JSON_COMMANDER] = {}
    decks_runs_random_items = {}
    decks_runs_random_items[MagicLoader.JSON_COMMANDER] = {}

    studied_decks[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED], \
    decks_runs_random_items[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED] = \
        prepare_deck_data(decks_loader, MagicLoader.JSON_COMMANDER, MagicLoader.CODE_RED, 1)

    set_catalog = set([])
    for deck in studied_decks[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED]:
        set_catalog = set_catalog.union(deck)
    card_catalog = list(set_catalog)

    print('Building model...')

    model = BPRKNN(card_catalog, studied_decks[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED])
    #best: LR: 0.1, decay 0.5, epoch_drop=50
    model.build_model(decks_runs_random_items[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED][0], N=5, lbd_I=0.05, lbd_J=0.01, learning_rate=0.1, epoch=100, batch_size=50, decay=0.5, nb_early_learning = 10, min_leaning_rate = 0.025)
    #model.build_model(decks_runs_random_items[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED][0], 10, lbd_I=0.05, lbd_J=0.01, learning_rate=0.1, epoch=100, batch_size=50, epochs_drop=200, decay=0.5)

    print('Evaluation synthesis:')
    scores = model.get_scores()
    for ep, score in enumerate(scores):
        print(str(ep) + '\t' + str(score[0]) + '\t' + str(score[1]))