import os
from topn_recommendations.utils import *
from loader.magic_loader import MagicLoader
from loader.deck_manager import DeckManager
from random import randint
from collections import deque

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

    runs_decks = deque()
    runs_random_items = deque()
    for i in range(nb_runs):
        random_items = deque()
        decks = deque()
        for deck in decks_to_prepare:
            index = randint(0, len(deck) - 1)
            random_items.append(deck[index])
            decks.append(deck[:])

        for j, card in enumerate(random_items):
            decks[j].remove(card)

        runs_decks.append(decks)
        runs_random_items.append(random_items)
    return runs_decks, runs_random_items

def build_magic_translators(catalog):
    encoder = {}
    decoder = {}
    for i, card in enumerate(catalog):
        encoder[card] = i
        decoder[i] = card
    return encoder, decoder

def encode(deck, encoder):
    encoded_deck = deque()
    for card in deck:
        encoded_deck.append(encoder[card])
    return encoded_deck

def decode(deck, decoder):
    decoded_deck = deque()
    for index in deck:
        decoded_deck.append(decoder[index])
    return decoded_deck

def add_deck_serie(training_serie, testing_serie, mode, color, decks_loader, nb_runs):
    if mode not in training_serie:
        training_serie[mode] = {}
        testing_serie[mode] = {}

    training_serie[mode][color], \
    testing_serie[mode][color] = \
        prepare_deck_data(decks_loader, mode, color, nb_runs)

def generate_card_catalog(decks_loader, mode, color):
    set_catalog = set([])
    for deck in decks_loader[mode].grouped_decks[color]:
        set_catalog = set_catalog.union(deck)
    return list(set_catalog)

def convert_multiverseid_to_ids(training_serie, testing_serie, encoder):
    converted_training_serie = {}
    converted_testing_serie = {}
    for mode in training_serie:
        for color in training_serie[mode]:
            train_decks = deque()
            for deck in training_serie[mode][color]:
                train_decks.append(encode(deck, encoder))

            test_decks = deque()
            for deck in testing_serie[mode][color]:
                test_decks.append(encode(deck, encoder))

            if mode not in converted_training_serie:
                converted_training_serie[mode] = {}
                converted_testing_serie[mode] = {}

            converted_training_serie[mode][color] = train_decks
            converted_testing_serie[mode][color] = test_decks
    return converted_training_serie, converted_testing_serie