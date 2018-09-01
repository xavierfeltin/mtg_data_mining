# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Utility functions for managing Magic cards and decks
#

import os
import json
from loader.magic_loader import MagicLoader
from loader.deck_manager import DeckManager

def load_magic_environment():
    '''
    Load all the magic cards information from AllSets-x.json database
    :return: Magic loader with all the cards information
    '''
    card_loader = MagicLoader()
    card_loader.load_from_set('./../data/magic_cards/AllSets-x.json')
    return card_loader

    card_loader = MagicLoader()
    card_loader.load('./../data/magic_cards/AllCards-x.json')
    return card_loader

def load_decks(card_loader, path='./../data/decks_mtgdeck_net_extended'):
    '''
    Load the decks from csv files (MTGDeck format) stored in path set in argument.
    :param card_loader: Magic loader containing all the cards information
    :param path: relative path to access the csv files
    :return: Hash of decks divided by modes then by colors
    '''
    files = os.listdir(path)  # returns list
    paths = []
    for file in files:
        paths.append(path + '/' + file)

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
    '''
    Extract the list of cards from the decks set in argument
    :param decks_loader: hash of decks split by mode and color
    :param card_loader: Magic loader containing all the cards information
    :return: list of cards contained in the deck
    '''
    multiverseid_in_decks = set()
    for mode in decks_loader:
        multiverseid_in_decks = multiverseid_in_decks.union(decks_loader[mode].cards)
    list_multiverseid_in_decks = list(multiverseid_in_decks)
    cards_in_decks = card_loader.extract_cards(list_multiverseid_in_decks)
    return cards_in_decks

def generate_card_catalog(decks_loader, mode, color):
    '''
    Return a list without duplicates of card's multiverseids of all the cards present in the decks matching
    the mode and the color set in arguments
    :param decks_loader: hash of decks split by mode and color
    :param mode: selected mode
    :param color: selected color
    :return: list of card's multiverseids in the selected decks
    '''
    set_catalog = set([])
    for deck in decks_loader[mode].grouped_decks[color]:
        set_catalog = set_catalog.union(deck)
    return list(set_catalog)

def save_catalog(catalog, card_loader, filename, path):
    '''
    Save the cards catalog into a json file
    :param catalog: list of cards multiverseid to save
    :param card_loader: Magic loader containing all the cards information
    :param filename: json file's name
    :param path: path to save the json file
    '''

    with open(path + '/' + filename + '.json', 'w') as f:
        json_data = []
        for multiverseid in catalog:
            json_data.append(card_loader.cards_multiverseid[multiverseid].to_json())
        json.dump(json_data, f)

def save_decks(decks, filename, path):
    '''
    Save the cards ids used in the decks into a json file
    :param deck: list of decks
    :param filename: json file's name
    :param path: path to save the json file
    '''
    with open(path + '/' + filename + '.json', 'w') as f:
        json_data = []
        for deck in decks:
            deck_data = []
            for multiverseid in deck:
                deck_data.append(multiverseid)
            json_data.append(deck_data)
        json.dump(json_data, f)