import os
import numpy as np
import matplotlib.pyplot as plt
from loader.loader_magic import MagicLoader, DeckManager

def load_magic_environment():
    print('Load deck')
    card_loader = MagicLoader()
    card_loader.load('./../data/magic_cards/AllCards-x.json')
    return card_loader

def load_magic_environment_from_set():
    print('Load deck')
    card_loader = MagicLoader()
    card_loader.load_from_set('./../data/magic_cards/AllSets-x.json')
    print('nb cards:' + str(len(card_loader.cards_multiverseid)))
    return card_loader

def load_decks_database(card_loader):
    print('Clean deck')
    deck_loader = DeckManager()

    files = os.listdir("./../data/decks_mtgdeck_net_extended")  # returns list
    paths = []
    for file in files:
        paths.append('./../data/decks_mtgdeck_net_extended/' + file)

    deck_loader.load_from_mtgdeck_csv(paths, card_loader)
    deck_loader.extract_lands(card_loader.lands, card_loader)
    deck_loader.sort_decks()

    return deck_loader

def plot_frequency():
    '''
    Plot the card frequency in the decks database
    '''

    print('Load magic environment')
    #card_loader = load_magic_environment()
    card_loader = load_magic_environment_from_set()
    deck_loader = load_decks_database(card_loader)

    nb_decks = len(deck_loader.decks)
    nb_cards = list(deck_loader.cards_frequency.values())

    for i in range(len(nb_cards)):
        nb_cards[i] = round(nb_cards[i] / nb_decks, 3)

    plt.hist(nb_cards, bins = 100)
    plt.ylabel('Number of cards')
    plt.xlabel('Support in decks')
    plt.show()

if __name__ == "__main__":
    plot_frequency()
