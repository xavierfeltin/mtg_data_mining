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

    #DECK GAME OFFICIAL MODES
    CODE_STANDARD = 1
    CODE_MODERN = 2
    CODE_LEGACY = 4
    CODE_VINTAGE = 8
    CODE_COMMANDER = 16

    JSON_STANDARD = 'Standard'
    JSON_MODERN = 'Modern'
    JSON_LEGACY = 'Legacy'
    JSON_VINTAGE = 'Vintage'
    JSON_COMMANDER = 'Commander'
    JSON_LEGAL = 'Legal'
    JSON_BANNED = 'Banned'

    GAME_MODES = [CODE_STANDARD, CODE_MODERN, CODE_LEGACY, CODE_VINTAGE, CODE_COMMANDER]
    HASH_GAME_CODE_STRING = {CODE_STANDARD: JSON_STANDARD, CODE_MODERN: JSON_MODERN, CODE_LEGACY: JSON_LEGACY, CODE_VINTAGE: JSON_VINTAGE, CODE_COMMANDER: JSON_COMMANDER}
    HASH_GAME_STRING_CODE = {JSON_STANDARD: CODE_STANDARD, JSON_MODERN: CODE_MODERN, JSON_LEGACY: CODE_LEGACY, JSON_VINTAGE: CODE_VINTAGE, JSON_COMMANDER: CODE_COMMANDER}

    #DECK COLORS
    CODE_WHITE = 1
    CODE_BLUE = 2
    CODE_BLACK = 4
    CODE_RED = 8
    CODE_GREEN = 16
    CODE_NO_COLOR = 32

    JSON_WHITE = 'W'
    JSON_BLUE = 'U'
    JSON_BLACK = 'B'
    JSON_RED = 'R'
    JSON_GREEN = 'G'

    STRING_WHITE = 'white'
    STRING_BLUE = 'blue'
    STRING_BLACK = 'black'
    STRING_RED = 'red'
    STRING_GREEN = 'green'
    STRING_NO_COLOR = 'no_color'

    COLORS = [CODE_WHITE, CODE_BLUE, CODE_BLACK, CODE_RED, CODE_GREEN, CODE_NO_COLOR]
    HASH_COLOR_CODE_STRING = {CODE_WHITE: STRING_WHITE, CODE_BLUE: STRING_BLUE, CODE_BLACK: STRING_BLACK, CODE_RED: STRING_RED, CODE_GREEN: STRING_GREEN, CODE_NO_COLOR: STRING_NO_COLOR}

    def __init__(self, file_type = 'card'):
        #self.texts = []
        self.hash_id_texts= {}
        self.names = []
        self.type = file_type
        self.lands = []
        self.hash_name_id = {}
        self.hash_id_name = {}
        self.special_indexes = []
        self.hash_id_mode = {} #can have several modes
        self.hash_id_color = {} #can have several colors

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

            self.set_color_identities(read_json, internal_id, card)
            self.set_legalities(read_json, internal_id, card)

        self.generate_dual_cards()

    def set_color_identities(self, read_json, internal_id, card):
        color_identity = self.get_field(read_json[card], 'colorIdentity')
        value = 0

        if color_identity == '':
            value = value | MagicLoader.CODE_NO_COLOR
        else:
            color_identity = color_identity.split(',')
            for color in color_identity:
                if color == MagicLoader.JSON_BLACK:
                    value = value | MagicLoader.CODE_BLACK
                elif color == MagicLoader.JSON_BLUE:
                    value = value | MagicLoader.CODE_BLUE
                elif color == MagicLoader.JSON_WHITE:
                    value = value | MagicLoader.CODE_WHITE
                elif color == MagicLoader.JSON_RED:
                    value = value | MagicLoader.CODE_RED
                elif color == MagicLoader.JSON_GREEN:
                    value = value | MagicLoader.CODE_GREEN
                else:
                    print('Error: ' + color + ' is not a valid color in Magic', file=sys.stderr)

        self.hash_id_color[internal_id] = value

    def set_legalities(self, read_json, internal_id, card):
        list_legalities = self.get_field(read_json[card], 'legalities')
        value = 0

        if list_legalities != '':
            for json_legality in list_legalities:
                game_format = self.get_field(json_legality, 'format')
                legality = self.get_field(json_legality, 'legality')

                if game_format == MagicLoader.JSON_STANDARD: #and legality == MagicLoader.JSON_LEGAL:
                    value = value | MagicLoader.CODE_STANDARD
                elif game_format == MagicLoader.JSON_LEGACY: # and legality == MagicLoader.JSON_LEGAL:
                    value = value | MagicLoader.CODE_LEGACY
                elif game_format == MagicLoader.JSON_MODERN: # and legality == MagicLoader.JSON_LEGAL:
                    value = value | MagicLoader.CODE_MODERN
                elif game_format == MagicLoader.JSON_VINTAGE: # and legality == MagicLoader.JSON_LEGAL:
                    value = value | MagicLoader.CODE_VINTAGE
                elif game_format == MagicLoader.JSON_COMMANDER: # and legality == MagicLoader.JSON_LEGAL:
                    value = value | MagicLoader.CODE_COMMANDER
                else:
                    pass #only official formats
        self.hash_id_mode[internal_id] = value

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

                #set color identity and legality using information of one of the two cards of the dual card
                internal_id = self.hash_name_id[names[0].strip()]
                self.hash_id_color[special_id] = self.hash_id_color[internal_id]
                self.hash_id_mode[special_id] = self.hash_id_mode[internal_id]
            else:
                self.hash_id_texts[special_id] = 'unknown'
                self.hash_id_color[special_id] = 100000
                self.hash_id_mode[special_id] = 11111

    def get_field(self, card_json, field):
        if field in card_json:
            if isinstance(card_json[field], list):
                if isinstance(card_json[field][0], str):
                    return ",".join(card_json[field])
                else:
                    return card_json[field]
            else:
                return card_json[field]
        else:
            return ''

    @staticmethod
    def get_json_color(color_to_convert):
        color = ''
        for i, code in enumerate(MagicLoader.COLORS):
            if color_to_convert & code != 0:
                color += MagicLoader.HASH_COLOR_CODE_STRING[code]
                color += '_'
        return color[0:len(color)-1]

class DeckManager:

    def __init__(self):
        self.decks = []
        self.cards = set()
        self.grouped_decks = {}
        self.grouped_cards = {}

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
                        color_identity = 0
                        game_mode = {}

                        process_deck = True
                        for index in error_index:
                            process_deck = process_deck and (int(row[index]) > 0)

                        if process_deck:
                            for i, nb_cards in enumerate(row):
                                if int(nb_cards) > 0 and i not in error_index:
                                    color_identity = color_identity | cards_loader.hash_id_color[file_cards[i]]

                                    if file_cards[i] not in deck:
                                        has_official_mode = False
                                        for mode in MagicLoader.GAME_MODES:
                                            if (mode & cards_loader.hash_id_mode[file_cards[i]] != 0) or cards_loader.hash_id_mode[file_cards[i]] == 0:
                                                has_official_mode = True
                                                if mode not in game_mode:
                                                    game_mode[mode] = 0
                                                game_mode[mode] += 1

                                        deck.append(file_cards[i])

                                        if not has_official_mode:
                                            print(card + ' is not in any official game mode!', file=sys.stderr)
                            self.decks.append(deck)

                            if color_identity & ~MagicLoader.CODE_NO_COLOR != 0:
                                # No color stay true if all cards are no color
                                color_identity = color_identity ^ MagicLoader.CODE_NO_COLOR

                            has_official_mode = False
                            for mode, nb_cards in game_mode.items():
                                if nb_cards == len(deck):
                                    has_official_mode = True
                                    if mode not in self.grouped_decks:
                                        self.grouped_decks[mode] = {}
                                        self.grouped_cards[mode] = {}

                                    if color_identity not in self.grouped_decks[mode]:
                                        self.grouped_decks[mode][color_identity] = []
                                        self.grouped_cards[mode][color_identity] = set([])

                                    self.grouped_decks[mode][color_identity].append(deck)
                                    self.grouped_cards[mode][color_identity] = self.grouped_cards[mode][
                                        color_identity].union(
                                        set(deck))

                            if not has_official_mode:
                                for card in deck:
                                    print(cards_loader.hash_id_name[card] + ', modes: ' + str(
                                        cards_loader.hash_id_mode[card]))
                                print('Deck not with official format', file=sys.stderr)
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
                file_cards = []
                error_index = []
                for row in rows:
                    if row != '""':
                        color_identity = 0

                        # Remove number of cards, unused in frequent items rule associations approach
                        csv_row = re.subn("( )?\d+ ",';', row)
                        csv_row = re.subn("\"", '', csv_row[0])
                        deck_cards = list(filter(None, csv_row[0].split(';')))

                        deck = []
                        for index, card in enumerate(deck_cards):
                            card = DeckManager.rename_card(card)
                            if card in list_cards:
                                if cards_loader:
                                    card_id = cards_loader.hash_name_id[card]
                                    color_identity = color_identity | cards_loader.hash_id_color[card_id]

                                    if card_id not in deck:
                                        file_cards.append(card_id)
                                        deck.append(card_id)
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