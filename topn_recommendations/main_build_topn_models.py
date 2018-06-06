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
from lsa.lsa_encoder import LSAManager
from collaborative_filtering.item_to_item import ItemToItem
from topn_recommendations.models.item_based_deshpande import ItemBasedDeshpande

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

def encoding_magic_card_subsets(cards):
    hash_id_texts = {}
    for card in cards:
        hash_id_texts[card.multiverseid] = card.full_text

    lsa_manager = LSAManager(hash_id_texts)
    lsa_manager.encode()
    return lsa_manager

if __name__ == "__main__":
    print('Load Magic environment')
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)
    lsa_manager = encoding_magic_card_subsets(get_cards_from_decks(decks_loader, card_loader))

    set_cards = set([])
    for mode in decks_loader.keys():
        set_cards = set_cards.union(decks_loader[mode].cards)
    card_catalog = list(set_cards)

    black_blue_green_red = MagicLoader.CODE_RED | MagicLoader.CODE_BLACK | MagicLoader.CODE_BLUE | MagicLoader.CODE_GREEN
    decks = decks_loader[MagicLoader.JSON_LEGACY].grouped_decks[black_blue_green_red]

    print('Building model...')
    # Model configuration
    k = 25
    alpha = 0.5
    norm_similarities = True
    model_similarities = ItemToItem.compute_cosine_angle_binary_lsa_row

    model = ItemBasedDeshpande(card_catalog, decks)
    model.build_model(k, model_similarities, lsa_manager, alpha, norm_similarities)

    print('Saving model...')
    filename = 'model_cosine_lsa_row_25_' + MagicLoader.JSON_LEGACY + '_' + str(black_blue_green_red)
    model.save_coefficients('./generated_models/' + filename)