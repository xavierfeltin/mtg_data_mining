# -*- coding: utf-8 -*-

import simplejson
import codecs
import csv
import operator
import sys
import re

def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

class MagicLoader:
    SPECIAL_INDEX = 30000 #Index to manage double cards
    DUAL_CARDS = ['Cut/Ribbons','Fire/Ice','Start/Finish','Rough/Tumble','Wear/Tear','Far/Away','Turn/Burn','Hit/Run','Appeal/Authority',
                 'Hide/Seek','Commit/Memory','Consign/Oblivion','Rise/Fall','Flesh/Blood','Boom/Bust','Struggle/Survive',
                 'Dead/Gone','Life/Death','Breaking/Entering','Farm/Market','Alive/Well','Reduce/Rubble','Grind/Dust','Claim/Fame',
                 'Driven/Despair','Ready/Willing','Crime/Punishment','Bound/Determined','Insult/Injury','Profit/Loss','Beck/Call',
                 'Never/Return','Dusk/Dawn','Spring/Mind','Onward/Victory','Dusk/Dawn','Never/Return','Heaven/Earth','Failure/Comply',
                 'Destined/Lead','Rags/Riches','Prepare/Fight','Rags/Riches','Toil/Trouble','Order/Chaos','Armed/Dangerous',
                 'Refuse/Cooperate','Reason/Believe','Leave/Chance','Mouth/Feed','Wax/Wane','Assault/Battery','Stand/Deliver',
                 'Spite/Malice','Trial/Error','Odds/Ends','Research/Development','Supply/Demand','Pain/Suffering','Catch/Release',
                 'Pure/Simple','Down/Dirty','Unknown Card']

    def __init__(self, file_type = 'card'):
        #self.texts = []
        self.hash_id_texts= {}
        self.names = []
        self.type = file_type
        self.lands = []
        self.hash_name_id = {}
        self.hash_id_name = {}
        self.special_indexes = []
        self.hash_id_mode = {}
        self.hash_id_color = {}

    def load(self, path):
        read_json = simplejson.load(open(path, "r", encoding='UTF-8'))

        for internal_id, card in enumerate(read_json):
            description = self.get_field(read_json[card], 'colors')
            description += ', ' + self.get_field(read_json[card], 'types')
            description += ', ' + self.get_field(read_json[card], 'subtypes')
            description += ', ' + self.get_field(read_json[card], 'power')
            description += ', ' + self.get_field(read_json[card], 'toughness')
            description += ', ' + self.get_field(read_json[card], 'text')
            #self.texts.append(description)
            self.hash_id_texts[internal_id] = description

            name = self.get_field(read_json[card], 'name')
            self.names.append(name)
            self.hash_name_id[name] = internal_id
            self.hash_id_name[internal_id] = name

            if self.get_field(read_json[card],'types') == 'Land':
                self.lands.append(self.get_field(read_json[card],'name'))
        self.generate_dual_cards()

    def generate_dual_cards(self):
        """
        Magic has cards with two faces. We can not know which face will be played in the deck.
        Special card are added to the original magic's card database to manage that
        """

        for i in range(len(MagicLoader.DUAL_CARDS)):
            special_id = MagicLoader.SPECIAL_INDEX + i
            self.special_indexes.append(MagicLoader.SPECIAL_INDEX + i)
            self.hash_id_name[special_id] =  MagicLoader.DUAL_CARDS[i]

            special_name = MagicLoader.DUAL_CARDS[i]
            if special_name != 'Unknown Card':
                items = special_name.split('/')
                special_name = items[0] + ' / ' + items[1]

            self.hash_name_id[special_name] = special_id

            if special_name != 'Unknown Card':
                names = special_name.split('/')
                description = ''
                for name in names:
                    name = name.strip()
                    id = self.hash_name_id[name]
                    add_coma = False
                    if len(description) == 0: add_coma = True
                    description += self.hash_id_texts[id]
                    if add_coma: description += ', '
                self.hash_id_texts[special_id] = description
            else:
                self.hash_id_texts[special_id] = 'unknown'

    def get_field(self, card_json, field):
        if field in card_json:
            if isinstance(card_json[field], list):
                return ",".join(card_json[field])
            else:
                return card_json[field]
        else:
            return ''

class DeckManager:

    #DECK GAME MODE
    STANDARD = 1
    MODERN = 10
    LEGACY = 100
    VINTAGE = 1000
    FRONTIER = 10000
    PAUPER = 100000
    COMMANDER = 1000000
    HIGHLANDER = 10000000
    MODES = [STANDARD, MODERN, LEGACY, VINTAGE, FRONTIER, PAUPER, COMMANDER, HIGHLANDER]

    #DECK COLORS
    WHITE = 1
    BLUE = 10
    BLACK = 100
    RED = 1000
    GREEN = 10000
    NO_COLOR = 100000
    COLORS = [WHITE, BLUE, BLACK, RED, GREEN, NO_COLOR]

    def __init__(self):
        self.decks = []
        self.cards = set()

    def load_from_csv(self, list_path, cards_loader = None):
        """
        Load decks from a list of csv files
        Decks are a list of the cards name building it
        If loader is set, match the cards with an internal ID
        """
        list_cards = []
        if cards_loader:
            list_cards = cards_loader.hash_name_id.keys()

        for file in list_path:
            with open('./../db_decks/' + file, newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                nb_line = 0
                file_cards = []
                error_index = []
                for row in reader:
                    if nb_line == 0:
                        for index, card in enumerate(row):
                            card = DeckManager.rename_card(card)
                            if card in list_cards:
                                if cards_loader:
                                    file_cards.append(cards_loader.hash_name_id[card])
                                else:
                                    file_cards.append(card)
                            else:
                                if card != 'Unknown Card':
                                    print('Error: ' + card + ' is not present in the Magic card database', file=sys.stderr)
                                error_index.append(index)
                                file_cards.append(card)
                    else:
                        deck = []
                        process_deck = True
                        for index in error_index:
                            process_deck = process_deck and (int(row[index]) > 0)

                        if process_deck:
                            for i, nb_cards in enumerate(row):
                                if int(nb_cards) > 0 and i not in error_index:
                                    deck.append(file_cards[i])
                            self.decks.append(deck)
                    nb_line+=1
                self.cards = set.union(self.cards, set(file_cards))

    def load_from_mtgdeck_csv(self,list_path,cards_loader = None):
        """
        Load decks from a list of csv files from MTGDECK website
        Decks are a list of the cards name building it
        If loader is set, match the cards with an internal ID
        """
        list_cards = []
        if cards_loader:
            list_cards = cards_loader.hash_name_id.keys()

        for file in list_path:
            print('file: ' + file)
            with open(file) as csvfile:
                reader = csvfile.read()
                rows = reader.split('\n')
                nb_line = 0
                file_cards = []
                error_index = []
                for row in rows:
                    # Remove number of cards, unused in frequent items rule associations approach
                    csv_row = re.subn("( )?\d+ ",';', row)
                    csv_row = re.subn("\"", '', csv_row[0])
                    deck_cards = list(filter(None, csv_row[0].split(';')))

                    deck = []
                    for index, card in enumerate(deck_cards):
                        card = DeckManager.rename_card(card)
                        if card in list_cards:
                            if cards_loader:
                                file_cards.append(cards_loader.hash_name_id[card])
                            else:
                                file_cards.append(card)
                        else:
                            if card != 'Unknown Card':
                                print('Error: ' + card + ' is not present in the Magic card database', file=sys.stderr)
                            error_index.append(index)
                            file_cards.append(card)

                        if file_cards[index] not in deck: deck.append(file_cards[index])
                    self.decks.append(deck)
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

    def extract_lands(self, land_cards, cards_loader):
        """
        Extract the lands from the decks
        """
        for deck in self.decks:
            for card in land_cards:
                if cards_loader.hash_name_id[card] in deck:
                    deck.remove(cards_loader.hash_name_id[card])

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