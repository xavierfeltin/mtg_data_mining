# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Main for generating models and saving them
#

from lsa.lsa_encoder import LSAManager
from collaborative_filtering.item_to_item import ItemToItem
from topn_recommendations.models.item_based_deshpande import ItemBasedDeshpande
from topn_recommendations.models.bpr_knn import BPRKNN
from topn_recommendations.utils import *


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

def generate_item_knn_model(card_catalog, mode, color, training_set):
    k = 25
    alpha = 0.5
    norm_similarities = True
    model_similarities = ItemToItem.compute_cosine_angle_binary_row
    model = ItemBasedDeshpande(card_catalog, training_set)
    model.build_model(k, model_similarities, lsa_manager, alpha, norm_similarities)

    print('Saving model...')
    filename = 'model_item_knn_cosine_' + mode + '_' + str(color) + '_' + str(k) + '.json'
    model.save_coefficients('./generated_models/' + filename)

def generate_bpr_knn_model(card_catalog, mode, color, training_set, testing_set):
    nb_runs = 1
    best_model = None
    for i in range(nb_runs):
        print('run ' + str(i))

        model = BPRKNN(card_catalog, training_set, testing_set)
        model.build_model(N=5, lbd_I=0.01,
                          lbd_J=0.005, learning_rate=0.1, epoch=200, batch_size=100, decay=0.5, nb_early_learning=20,
                          min_leaning_rate=0.025, normalize=True)

        if best_model is None:
            best_model = model
        else:
            if best_model.get_scores()[-1][0] < model.get_scores()[-1][0]:
                best_model = model
            elif best_model.get_scores()[-1][0] == model.get_scores()[-1][0] and best_model.get_scores()[-1][1] < model.get_scores()[-1][1]:
                best_model = model

    print('Saving model...')
    filename = 'model_bpr_knn_' + mode + '_' + str(color) + '_string.json'
    best_model.save_string_coefficients('./generated_models/' + filename)


if __name__ == "__main__":
    print('Load Magic environment')
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)
    lsa_manager = encoding_magic_card_subsets(get_cards_from_decks(decks_loader, card_loader))

    set_cards = set([])
    for mode in decks_loader.keys():
        set_cards = set_cards.union(decks_loader[mode].cards)
    card_catalog = list(set_cards)

    studied_decks = {}
    decks_runs_random_items = {}

    color = MagicLoader.CODE_RED | MagicLoader.CODE_BLACK | MagicLoader.CODE_BLUE | MagicLoader.CODE_GREEN
    mode = MagicLoader.JSON_LEGACY
    add_deck_serie(studied_decks, decks_runs_random_items, mode, color, decks_loader, 1)
    card_catalog = generate_card_catalog(decks_loader, mode, color)

    print('Building model...')
    #generate_item_knn_model(card_catalog, mode, color, studied_decks[mode][color][0])
    generate_bpr_knn_model(card_catalog, mode, color,  studied_decks[mode][color][0], decks_runs_random_items[mode][color][0])
    
