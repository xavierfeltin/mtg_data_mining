# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Main for generating recommendations from a set of selected cards
#

import os

from loader.magic_loader import MagicLoader
from loader.deck_manager import DeckManager
from topn_recommendations.models.bpr_knn import BPRKNN

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

if __name__ == "__main__":
    print('Load Magic environment')
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)

    blue_white = MagicLoader.CODE_BLUE | MagicLoader.CODE_WHITE
    decks = decks_loader[MagicLoader.JSON_STANDARD].grouped_decks[blue_white]

    print('Getting recommendations for :')

    #Example of deck from https://deckstats.net/decks/629/1008688-czech-pile/en
    built_decks = [3897, 414380, 27251, 423724, 3107, 1852, 195297, 394613, 806, 414388, 139512, 205019, 4083, 145969, 409889, 430619, 290529, 416834, 227676]

    hash_card_support = {}
    hash_card_support = {}
    for multiverseid in built_decks:
        hash_card_support[multiverseid] = 0

    targeted_decks = set([])
    for index, deck in enumerate(decks):
        count = 0
        for multiverseid in built_decks:
            if multiverseid in deck:
                count += 1
                hash_card_support[multiverseid] += 1
                targeted_decks = targeted_decks.union([index])

            if count == len(built_decks):
                print('(sub)deck exist in training set')

    for multiverseid in built_decks:
        card = card_loader.cards_multiverseid[int(multiverseid)]
        print('  - ' + str(card.multiverseid) + ' - ' + card.name + ' - support: ' + str(hash_card_support[multiverseid]))  # Expect Goblins
    print('Cards represented in ' + str(len(targeted_decks)) + ' decks')

    n = 10
    print('BPR KNN:')
    filename = 'Standard_Blue_White_bprknn.json'
    model = BPRKNN.load_coefficients_from_string('./generated_models/' + filename)
    recommendations = model.get_top_N_recommendations(built_decks, n)
    contributions = model.get_contributions(recommendations.index, built_decks, max_contributors = 10, thresold=0.1)

    for multiverseid, score in recommendations.iteritems():
        card = card_loader.cards_multiverseid[int(multiverseid)]
        if len(contributions[int(multiverseid)]) > 0:
            contrib_cards = ', '.join(map(lambda x: card_loader.cards_multiverseid[x[0]].name + '(' + str(round(x[1]*100.0, 2)) + '%)', contributions[multiverseid]))
        else:
            contrib_cards = 'global contribution'
        print('  - ' + str(card.multiverseid) + ' - ' + card.name + ', because you selected: ' + contrib_cards)

    '''    
    print('Item KNN:')
    k = 25
    filename = 'model_item_knn_cosine_' + MagicLoader.JSON_LEGACY + '_' + str(black_blue_green_red) + '_' + str(k) + '.json'
    model = ItemBasedDeshpande.load_coefficients('./generated_models/' + filename)
    recommendations = model.get_top_N_recommendations(built_decks, n)
    contributions = model.get_contributions(recommendations.index, built_decks, max_contributors = 10)

    for multiverseid, score in recommendations.iteritems():
        card = card_loader.cards_multiverseid[int(multiverseid)]
        if len(contributions[int(multiverseid)]) > 0:
            contrib_cards = ', '.join(
                map(lambda x: card_loader.cards_multiverseid[x[0]].name + '(' + str(round(x[1] * 100.0, 2)) + '%)',
                    contributions[multiverseid]))
        else:
            contrib_cards = 'global contribution'

        print('  - ' + str(card.multiverseid) + ' - ' + card.name + ', because you selected: ' + contrib_cards)
    '''