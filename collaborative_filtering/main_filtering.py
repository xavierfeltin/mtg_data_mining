import os
import json
from loader_magic import MagicLoader, DeckManager
from collaborative_filtering.item_to_item import ItemToItem
from lsa_encoder import DataCleaner, LSAEncoder, LSAManager

def encoding_magic_card(card_loader):
    lsa_manager = LSAManager(card_loader.hash_id_texts)
    lsa_manager.encode()
    return lsa_manager

def load_magic_environment():
    print('Load deck')
    card_loader = MagicLoader()
    card_loader.load('./../data/magic_cards/AllCards-x.json')
    return card_loader

def load_decks_database(card_loader):
    print('Clean deck')
    deck_loader = DeckManager()

    files = os.listdir("./../data/decks_mtgdeck_net")  # returns list
    paths = []
    for file in files:
        paths.append('./../data/decks_mtgdeck_net/' + file)
    deck_loader.load_from_mtgdeck_csv(paths, card_loader)
    deck_loader.extract_lands(card_loader.lands, card_loader)

    '''
    list_files = os.listdir("./../db_decks")  # returns list
    deck_loader.load_from_csv(list_files, card_loader)
    deck_loader.extract_lands(card_loader.lands, card_loader)
    '''

    return deck_loader

if __name__ == "__main__":
    print('Load magic environment')
    card_loader = load_magic_environment()
    deck_loader = load_decks_database(card_loader)

    print('Convert card text into vector')
    lsa_manager = encoding_magic_card(card_loader)

    catalog = sorted(list(deck_loader.cards))
    item_recommender = ItemToItem(list(deck_loader.cards))
    print('Get ratings')
    item_recommender.load_ratings(deck_loader.decks)
    print('Compute similarities')
    item_recommender.compute_similarities(deck_loader.decks)

    filename = ''
    similiraties = {}
    for id_card in catalog:
        recommendations = item_recommender.get_recommendation(id_card, 5, lsa_manager)
        suggestions = {}
        for id_rec, score in recommendations.items():
            suggestions[card_loader.hash_id_name[id_rec]] = {'item_similarity': score[0], 'content_similarity': score[1]}
        similiraties[card_loader.hash_id_name[id_card]] = suggestions

    with open('./../similarities.json', 'w') as f:
        json.dump(similiraties, f)

    '''
    print('Get recommendations for 16622')
    recommendations = item_recommender.get_recommendation(16622, 10, lsa_manager)
    print('Recommendation for ' + str(card_loader.hash_id_name[16622]) + ':')#16622, 620
    for id_card, score in recommendations.items():
        print('   - ' + str(card_loader.hash_id_name[id_card]) + ': ' + str(score))

    print('Get recommendations for 620')
    recommendations = item_recommender.get_recommendation(620, 10, lsa_manager)
    print('Recommendation for ' + str(card_loader.hash_id_name[620]) + ':')#16622, 620
    for id_card, score in recommendations.items():
        print('   - ' + str(card_loader.hash_id_name[id_card]) + ': ' + str(score))
    '''