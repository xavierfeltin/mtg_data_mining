import json
import csv
import operator

class MagicLoader:
    def __init__(self, file_type = 'card'):
        self.texts = []
        self.names = []
        self.type = file_type
        self.lands = []

    def load(self, path):
        read_json = json.load(open(path))

        for card in read_json:
            description = self.get_field(read_json[card], 'colors')
            description += ', ' + self.get_field(read_json[card], 'types')
            description += ', ' + self.get_field(read_json[card], 'subtypes')
            description += ', ' + self.get_field(read_json[card], 'power')
            description += ', ' + self.get_field(read_json[card], 'toughness')
            description += ', ' + self.get_field(read_json[card], 'text')
            self.texts.append(description)
            self.names.append(self.get_field(read_json[card], 'name'))

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

    def load_from_csv(self, list_path):
        """
        Load decks from a list of csv files
        Decks are a list of the cards name building it
        """

        for file in list_path:
            with open('./db_decks/' + file, newline='\n') as csvfile:
                reader = csv.reader(csvfile, delimiter=';')
                nb_line = 0
                file_cards = []
                for row in reader:
                    if nb_line == 0:
                        for card in row:
                            file_cards.append(card)
                    else:
                        deck = []
                        for i, nb_cards in enumerate(row):
                            if int(nb_cards) > 0 : deck.append(file_cards[i])
                        self.decks.append(deck)
                    nb_line+=1
                self.cards = set.union(self.cards, set(file_cards))

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




