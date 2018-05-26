# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#

import simplejson
import sys
from collections import deque
from loader.card import Card

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
    CODE_PAUPER = 32

    JSON_STANDARD = 'Standard'
    JSON_MODERN = 'Modern'
    JSON_LEGACY = 'Legacy'
    JSON_VINTAGE = 'Vintage'
    JSON_COMMANDER = 'Commander'
    JSON_PAUPER = 'Pauper'
    JSON_LEGAL = 'Legal'
    JSON_BANNED = 'Banned'

    GAME_MODES = [CODE_STANDARD, CODE_MODERN, CODE_LEGACY, CODE_VINTAGE, CODE_COMMANDER, CODE_PAUPER]
    HASH_GAME_CODE_STRING = {CODE_STANDARD: JSON_STANDARD, CODE_MODERN: JSON_MODERN, CODE_LEGACY: JSON_LEGACY, CODE_VINTAGE: JSON_VINTAGE, CODE_COMMANDER: JSON_COMMANDER, CODE_PAUPER: JSON_PAUPER}
    HASH_GAME_STRING_CODE = {JSON_STANDARD: CODE_STANDARD, JSON_MODERN: CODE_MODERN, JSON_LEGACY: CODE_LEGACY, JSON_VINTAGE: CODE_VINTAGE, JSON_COMMANDER: CODE_COMMANDER, JSON_PAUPER: CODE_PAUPER}

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
    STRING_NO_COLOR = 'no color'

    COLORS = [CODE_WHITE, CODE_BLUE, CODE_BLACK, CODE_RED, CODE_GREEN, CODE_NO_COLOR]
    HASH_COLOR_CODE_STRING = {CODE_WHITE: STRING_WHITE, CODE_BLUE: STRING_BLUE, CODE_BLACK: STRING_BLACK, CODE_RED: STRING_RED, CODE_GREEN: STRING_GREEN, CODE_NO_COLOR: STRING_NO_COLOR}

    NO_MULTIVERSEID = -1

    def __init__(self, file_type = 'card'):
        #self.texts = []
        self.hash_id_texts= {}
        self.names = []
        self.type = file_type
        self.lands = []
        self.hash_name_id = {}
        self.hash_id_name = {}
        self.special_indexes = []
        self.hash_id_color = {} #can have several colors
        self.cards_multiverseid = {}
        self.cards_name = {}

    def load(self, path):
        """
        Load cards from AllCards-x-json from MTGJson
        :param path: path to json file
        :return: none
        """
        read_json = simplejson.load(open(path, "r", encoding='UTF-8'))

        for internal_id, card in enumerate(read_json):
            description = MagicLoader.get_field(read_json[card], 'colors')
            description += ', ' + MagicLoader.get_field(read_json[card], 'types')
            description += ', ' + MagicLoader.get_field(read_json[card], 'subtypes')
            description += ', ' + MagicLoader.get_field(read_json[card], 'power')
            description += ', ' + MagicLoader.get_field(read_json[card], 'toughness')
            description += ', ' + MagicLoader.get_field(read_json[card], 'text')
            #self.texts.append(description)
            self.hash_id_texts[internal_id] = description

            name = MagicLoader.get_field(read_json[card], 'name')
            self.names.append(name)
            self.hash_name_id[name] = internal_id
            self.hash_id_name[internal_id] = name

            if MagicLoader.get_field(read_json[card],'types') == 'Land':
                self.lands.append(self.get_field(read_json[card],'name'))

            self.set_color_identities(read_json, internal_id, card)

        self.generate_dual_cards()

    def load_from_set(self, path):
        """
        Load cards from AllSets-x-json from MTGJson
        :param path: path to json file
        :return: none
        """
        read_json = simplejson.load(open(path, "r", encoding='UTF-8'))
        set_lands = set()
        for extension_name in read_json:
            extension = read_json[extension_name]
            for json_card in extension['cards']:
                if 'multiverseid' in json_card and json_card['multiverseid'] not in self.cards_multiverseid:
                    #cards not from Gatherer extensions do not have multiverseid
                    full_text = MagicLoader.get_field(json_card, 'colors')
                    full_text += ', ' + MagicLoader.get_field(json_card, 'types')
                    full_text += ', ' + MagicLoader.get_field(json_card, 'subtypes')
                    full_text += ', ' + MagicLoader.get_field(json_card, 'power')
                    full_text += ', ' + MagicLoader.get_field(json_card, 'toughness')
                    full_text += ', ' + MagicLoader.get_field(json_card, 'text')

                    if 'colorIdentity' in json_card:
                        colors = json_card['colorIdentity']
                    else:
                        colors = []

                    if 'types' in json_card:
                        types = json_card['types']
                    else:
                        types = []

                    card = Card(json_card['multiverseid'], json_card['name'], json_card['cmc'], types, colors, full_text, MagicLoader.get_field(json_card, 'text'))
                    self.cards_multiverseid[card.multiverseid] = card
                    self.cards_name[card.name] = card

                    if 'Land' in types:
                        set_lands = set_lands.union([card.multiverseid])

        self.lands = list(set_lands)
        self.add_dual_cards()

    def set_color_identities(self, read_json, internal_id, card):
        """
        Encode colors read into json into a binary format into self.hash_id_color
        :param read_json: json data
        :param internal_id: id of the card used as key for self.hash_id_color
        :param card: card value
        :return: none
        """
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
            else:
                self.hash_id_texts[special_id] = 'unknown'
                self.hash_id_color[special_id] = 100000

    def add_dual_cards(self):
        """
        Magic has cards with two faces. We can not know which face will be played in the deck.
        Special card are added to the original magic's card database to manage that
        Replace their original card
        """

        for i in range(len(MagicLoader.DUAL_CARDS)):
            special_name = MagicLoader.DUAL_CARDS[i]
            if special_name != 'Unknown Card':
                items = special_name.split('/')
                special_name = items[0] + ' / ' + items[1]
                first_name = items[0]
                reference_card = self.cards_name[first_name]
                dual_card = Card(reference_card.multiverseid, special_name, reference_card.mana_cost, reference_card.types, reference_card.colors, reference_card.full_text, reference_card.description)
                self.cards_multiverseid[dual_card.multiverseid] = dual_card
                self.cards_name[dual_card.name] = dual_card

    def extract_cards(self, multiverseids):
        '''
        Return a list of cards matching the multiverseids in argument
        :param multiverseids: list of searched multiverseids
        :return: list of cards
        '''
        extraction = deque()
        for id in multiverseids:
            if id in self.cards_multiverseid:
                extraction.append(self.cards_multiverseid[id])

        return extraction

    @staticmethod
    def get_field(card_json, field):
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
        """
        Convert color from binary format to string format
        :param color_to_convert: binary color
        :return: string
        """
        color = ''
        for i, code in enumerate(MagicLoader.COLORS):
            if color_to_convert & code != 0:
                color += MagicLoader.HASH_COLOR_CODE_STRING[code]
                color += '_'
        return color[0:len(color)-1]