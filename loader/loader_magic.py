# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#

import csv
import operator
import sys
import re
from loader.magic_loader import MagicLoader

class DeckManager:

    def __init__(self):
        self.decks = []
        self.cards = set()
        self.grouped_decks = {}
        self.grouped_cards = {}
        self.cards_frequency = {}

    def load_from_mtgdeck_csv(self,list_path,cards_loader = None, ignore_land = False):
        """
        Load decks from a list of csv files from MTGDECK website
        Decks are a list of the cards name building it
        If loader is set, match the cards with an internal ID
        """
        list_cards = []
        if cards_loader:
            #list_cards = cards_loader.hash_name_id.keys()
            list_cards = cards_loader.cards_name.keys()

        for file in list_path:
            print('file: ' + file)
            with open(file) as csvfile:
                reader = csvfile.read()
                rows = reader.split('\n')
                file_cards = []
                error_index = []
                for row in rows:
                    if len(row) == 0 or row != '""':
                        color_identity = 0

                        # Remove number of cards, unused in frequent items rule associations approach
                        csv_row = re.subn("( )?\d+ ",';', row)
                        csv_row = re.subn("\"", '', csv_row[0])
                        deck_cards = list(filter(None, csv_row[0].split(';')))

                        deck = []
                        for index, card in enumerate(deck_cards):
                            card = DeckManager.rename_card(card)
                            if card in list_cards:
                                reference_card = cards_loader.cards_name[card]
                                if not ignore_land or (ignore_land and not reference_card.is_basic_land()):
                                    if cards_loader:
                                        #card_id = cards_loader.hash_name_id[card]
                                        card_id = reference_card.multiverseid
                                        #color_identity = color_identity | cards_loader.hash_id_color[card_id]
                                        color_identity = color_identity | reference_card.code_color

                                        if card_id not in deck:
                                            file_cards.append(card_id)
                                            deck.append(card_id)

                                        if card_id in self.cards_frequency:
                                            self.cards_frequency[card_id] += 1
                                        else:
                                            self.cards_frequency[card_id] = 1
                                    else:
                                        file_cards.append(card)
                                        deck.append(card)
                            else:
                                if card != 'Unknown Card':
                                    print('Error: ' + card + ' is not present in the Magic card database', file=sys.stderr)
                                else:
                                    print('Warning: ' + card + ' present', file=sys.stderr)
                                error_index.append(index)
                                file_cards.append(card)
                                deck.append(card)

                        self.decks.append(deck) #remove duplicates

                        if color_identity & ~MagicLoader.CODE_NO_COLOR != 0 and color_identity & MagicLoader.CODE_NO_COLOR != 0:
                            # No color stay true if all cards are no color
                            color_identity = color_identity ^ MagicLoader.CODE_NO_COLOR

                        if color_identity not in self.grouped_decks:
                            self.grouped_decks[color_identity] = []
                            self.grouped_cards[color_identity] = set([])

                        self.grouped_decks[color_identity].append(deck)
                        self.grouped_cards[color_identity] = self.grouped_cards[color_identity].union(set(deck))

                self.cards = set.union(self.cards, set(file_cards))

    @staticmethod
    def rename_card(card):
        "Adapt card name to the reference database"
        if card == 'Stone golem':
            return 'Stone Golem'
        if card in MagicLoader.DUAL_CARDS and card != 'Unknown Card':
            items = card.split('/')
            return items[0].strip() + ' / ' + items[1].strip()
        else:
            return card

    def extract_high_used_cards(self, cards_usage, max_usage):
        """
        Extract the cards with a high usage in the database
        :param cards_usage: number of times the card is present in all decks
        :param max_usage: thresold
        """

        ordered_cards_usage = sorted(cards_usage.items(), key=operator.itemgetter(1), reverse=True)
        for deck in self.decks:
            i = 0
            while ordered_cards_usage[i][1] >= max_usage:
                card = list(ordered_cards_usage[i][0])[0]
                if card in deck:
                    deck.remove(card)
                i+=1

    def write_frequent_items_into_csv(self, filename, freqIDItemList, card_loader):
        with open('./output/' + filename + '.csv', 'w', newline='') as csvfile:
            writer = csv.writer(csvfile, delimiter=';', quotechar='|', quoting=csv.QUOTE_MINIMAL)

            writer.writerow(['Frequent set of cards'])
            for itemList in freqIDItemList:
                line = []
                for item in itemList:
                    line.append(card_loader.hash_id_name[item])
                writer.writerow(line)

    def sort_decks(self):
        '''
        Sort decks by card ids
        '''
        for deck in self.decks:
            deck.sort()