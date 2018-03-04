# -*- coding: utf-8 -*-

import simplejson
import codecs
import csv
import operator
import sys

class MagicLoader:
    SPECIAL_INDEX = 30000 #Index to manage double cards

    def __init__(self, file_type = 'card'):
        self.texts = []
        #self.names = []
        self.type = file_type
        self.lands = []
        self.hash_name_id = {}
        self.hash_id_name = {}

    def load(self, path):
        read_json = simplejson.load(open(path, "r", encoding='UTF-8'))

        self.generate_dual_cards()
        for internal_id, card in enumerate(read_json):
            description = self.get_field(read_json[card], 'colors')
            description += ', ' + self.get_field(read_json[card], 'types')
            description += ', ' + self.get_field(read_json[card], 'subtypes')
            description += ', ' + self.get_field(read_json[card], 'power')
            description += ', ' + self.get_field(read_json[card], 'toughness')
            description += ', ' + self.get_field(read_json[card], 'text')
            self.texts.append(description)

            name = self.get_field(read_json[card], 'name')
            #self.names.append(name)
            self.hash_name_id[name] = internal_id
            self.hash_id_name[internal_id] = name

            if self.get_field(read_json[card],'types') == 'Land':
                self.lands.append(self.get_field(read_json[card],'name'))

    def generate_dual_cards(self):
        """
        Magic has cards with two faces. We can not know which face will be played in the deck.
        Special card are added to the original magic's card database to manage that
        """
        self.hash_name_id['Cut / Ribbons'] = MagicLoader.SPECIAL_INDEX
        self.hash_name_id['Fire / Ice'] = MagicLoader.SPECIAL_INDEX + 1
        self.hash_name_id['Start / Finish'] = MagicLoader.SPECIAL_INDEX + 2
        self.hash_name_id['Rough / Tumble'] = MagicLoader.SPECIAL_INDEX + 3
        self.hash_name_id['Wear / Tear'] = MagicLoader.SPECIAL_INDEX + 4
        self.hash_name_id['Far / Away'] = MagicLoader.SPECIAL_INDEX + 4
        self.hash_name_id['Turn / Burn'] = MagicLoader.SPECIAL_INDEX + 5
        self.hash_name_id['Hit / Run'] = MagicLoader.SPECIAL_INDEX + 6
        self.hash_name_id['Appeal / Authority'] = MagicLoader.SPECIAL_INDEX + 7
        self.hash_name_id['Hide / Seek'] = MagicLoader.SPECIAL_INDEX + 8
        self.hash_name_id['Commit / Memory'] = MagicLoader.SPECIAL_INDEX + 9
        self.hash_name_id['Consign / Oblivion'] = MagicLoader.SPECIAL_INDEX + 10
        self.hash_name_id['Rise / Fall'] = MagicLoader.SPECIAL_INDEX + 11
        self.hash_name_id['Flesh / Blood'] = MagicLoader.SPECIAL_INDEX + 12
        self.hash_name_id['Boom / Bust'] = MagicLoader.SPECIAL_INDEX + 13
        self.hash_name_id['Struggle / Survive'] = MagicLoader.SPECIAL_INDEX + 14
        self.hash_name_id['Dead / Gone'] = MagicLoader.SPECIAL_INDEX + 15
        self.hash_name_id['Life / Death'] = MagicLoader.SPECIAL_INDEX + 16
        self.hash_name_id['Breaking / Entering'] = MagicLoader.SPECIAL_INDEX + 17
        self.hash_name_id['Farm / Market'] = MagicLoader.SPECIAL_INDEX + 18
        self.hash_name_id['Alive / Well'] = MagicLoader.SPECIAL_INDEX + 19
        self.hash_name_id['Reduce / Rubble'] = MagicLoader.SPECIAL_INDEX + 20
        self.hash_name_id['Grind / Dust'] = MagicLoader.SPECIAL_INDEX + 21
        self.hash_name_id['Claim / Fame'] = MagicLoader.SPECIAL_INDEX + 22
        self.hash_name_id['Driven / Despair'] = MagicLoader.SPECIAL_INDEX + 23
        self.hash_name_id['Ready / Willing'] = MagicLoader.SPECIAL_INDEX + 24
        self.hash_name_id['Crime / Punishment'] = MagicLoader.SPECIAL_INDEX + 25
        self.hash_name_id['Bound / Determined'] = MagicLoader.SPECIAL_INDEX + 26
        self.hash_name_id['Insult / Injury'] = MagicLoader.SPECIAL_INDEX + 27
        self.hash_name_id['Profit / Loss'] = MagicLoader.SPECIAL_INDEX + 28
        self.hash_name_id['Beck / Call'] = MagicLoader.SPECIAL_INDEX + 29
        self.hash_name_id['Never / Return'] = MagicLoader.SPECIAL_INDEX + 30
        self.hash_name_id['Dusk / Dawn'] = MagicLoader.SPECIAL_INDEX + 31
        self.hash_name_id['Spring / Mind'] = MagicLoader.SPECIAL_INDEX + 32
        self.hash_name_id['Onward / Victory'] = MagicLoader.SPECIAL_INDEX + 33
        self.hash_name_id['Dusk / Dawn'] = MagicLoader.SPECIAL_INDEX + 34
        self.hash_name_id['Never / Return'] = MagicLoader.SPECIAL_INDEX + 35
        self.hash_name_id['Heaven / Earth'] = MagicLoader.SPECIAL_INDEX + 36
        self.hash_name_id['Failure / Comply'] = MagicLoader.SPECIAL_INDEX + 37
        self.hash_name_id['Destined / Lead'] = MagicLoader.SPECIAL_INDEX + 38
        self.hash_name_id['Rags / Riches'] = MagicLoader.SPECIAL_INDEX + 39
        self.hash_name_id['Prepare / Fight'] = MagicLoader.SPECIAL_INDEX + 40
        self.hash_name_id['Rags / Riches'] = MagicLoader.SPECIAL_INDEX + 41
        self.hash_name_id['Toil / Trouble'] = MagicLoader.SPECIAL_INDEX + 42
        self.hash_name_id['Order / Chaos'] = MagicLoader.SPECIAL_INDEX + 43
        self.hash_name_id['Armed / Dangerous'] = MagicLoader.SPECIAL_INDEX + 44
        self.hash_name_id['Refuse / Cooperate'] = MagicLoader.SPECIAL_INDEX + 45
        self.hash_name_id['Reason / Believe'] = MagicLoader.SPECIAL_INDEX + 46
        self.hash_name_id['Leave / Chance'] = MagicLoader.SPECIAL_INDEX + 47
        self.hash_name_id['Mouth / Feed'] = MagicLoader.SPECIAL_INDEX + 48
        self.hash_name_id['Wax / Wane'] = MagicLoader.SPECIAL_INDEX + 49
        self.hash_name_id['Assault / Battery'] = MagicLoader.SPECIAL_INDEX + 50
        self.hash_name_id['Stand / Deliver'] = MagicLoader.SPECIAL_INDEX + 51
        self.hash_name_id['Spite / Malice'] = MagicLoader.SPECIAL_INDEX + 52
        self.hash_name_id['Trial / Error'] = MagicLoader.SPECIAL_INDEX + 53
        self.hash_name_id['Odds / Ends'] = MagicLoader.SPECIAL_INDEX + 54
        self.hash_name_id['Research / Development'] = MagicLoader.SPECIAL_INDEX + 55
        self.hash_name_id['Supply / Demand'] = MagicLoader.SPECIAL_INDEX + 56
        self.hash_name_id['Pain / Suffering'] = MagicLoader.SPECIAL_INDEX + 57
        self.hash_name_id['Catch / Release'] = MagicLoader.SPECIAL_INDEX + 58
        self.hash_name_id['Pure / Simple'] = MagicLoader.SPECIAL_INDEX + 59
        self.hash_name_id['Down / Dirty'] = MagicLoader.SPECIAL_INDEX + 60

    def get_field(self, card_json, field):
        if field in card_json:
            if isinstance(card_json[field], list):
                return ",".join(card_json[field])
            else:
                return card_json[field]
        else:
            return ''

class DeckManager:
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
            with open('./db_decks/' + file, newline='\n') as csvfile:
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

    @staticmethod
    def rename_card(card):
        "Adapt card name to the reference database"
        if card == 'Stone golem':
            return 'Stone Golem'
        else:
            return card

    def extract_lands(self, land_cards):
        """
        Extract the lands from the decks
        """
        for deck in self.decks:
            for card in land_cards:
                if card in deck:
                    deck.remove(card)

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
                    line.append(card_loader.hash_name_id[item])
                writer.writerow(line)