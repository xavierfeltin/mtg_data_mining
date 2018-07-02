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
from topn_recommendations.models.item_based_deshpande import ItemBasedDeshpande
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

    black_blue_green_red = MagicLoader.CODE_RED | MagicLoader.CODE_BLACK | MagicLoader.CODE_BLUE | MagicLoader.CODE_GREEN
    decks = decks_loader[MagicLoader.JSON_LEGACY].grouped_decks[black_blue_green_red]

    print('Getting recommendations for :')
    # https://deckstats.net/decks/629/1008688-czech-pile/en
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

    #filename = 'model_cosine_lsa_row_25_' + MagicLoader.JSON_LEGACY + '_' + str(black_blue_green_red)
    #model = ItemBasedDeshpande.load_coefficients('./generated_models/' + filename)

    filename = 'model_bpr_knn_' + MagicLoader.JSON_LEGACY + '_' + str(black_blue_green_red) + '.json'
    model = BPRKNN.load_coefficients('./generated_models/' + filename)

    n = 10
    recommendations = model.get_top_N_recommendations(built_decks, n)
    for multiverseid, score in recommendations.iteritems():
        card = card_loader.cards_multiverseid[int(multiverseid)]
        print('  - ' + str(card.multiverseid) + ' - ' + card.name)