import json
import csv
import operator

class MagicLoader:
    def __init__(self, file_type = 'card'):
        self.texts = []
        #self.names = []
        self.type = file_type
        self.lands = []
        self.hash_name_id = {}
        self.hash_id_name = {}

    def load(self, path):
        read_json = json.load(open(path))

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

        for file in list_path:
            with open('./db_decks/' + file, newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                nb_line = 0
                file_cards = []
                for row in reader:
                    if nb_line == 0:
                        for card in row:
                            card = DeckManager.rename_card(card)
                            card_id = card
                            if cards_loader is not None:
                                card_id = cards_loader.hash_name_id[card]
                            file_cards.append(card_id)
                    else:
                        deck = []
                        for i, nb_cards in enumerate(row):
                            if int(nb_cards) > 0 : deck.append(file_cards[i])
                        self.decks.append(deck)
                    nb_line+=1
                self.cards = set.union(self.cards, set(file_cards))

    @staticmethod
    def rename_card(name):
        if name == 'Cut / Ribbons':
            return 'Ribbons'
        elif name == 'Fire / Ice':
            return 'Fire' #could be Ice as well ... no way to know
        elif name == 'Start / Finish':
            return 'Start'  # could be Finish as well ... no way to know
        elif name == 'Wear / Tear':
            return 'Wear'  # could be Tear as well ... no way to know
        elif name == 'Rough / Tumble':
            return 'Rough'  # could be Tumble as well ... no way to know
        elif name == 'Unkown Card':
            return ''
        else:
            return name

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




