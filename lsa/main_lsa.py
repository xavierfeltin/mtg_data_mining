# -*- coding: utf-8 -*-
import pandas as pd
import json
from loader.loader_magic import MagicLoader, DeckManager
from lsa.lsa_encoder import DataCleaner, LSAEncoder, LSAManager

def encoding_magic_card(card_loader):
    lsa_manager = LSAManager(card_loader.hash_id_texts)
    lsa_manager.encode()
    return lsa_manager

def load_magic_environment():
    print('Load deck')
    card_loader = MagicLoader()
    card_loader.load('./../data/magic_cards/AllCards-x.json')
    return card_loader

def print_similarities(lsa_manager):
    lsa_manager.encoder.print_similarity()

def print_similarities_card(card_name, nb_recommendations, lsa_manager, card_loader):
    '''
    Generate a json with the best nb_recommendations based on content similarity to the card given in argument
    :param card_name: name of the card
    :param nb_recommendations: number of the recommendations
    :param lsa_manager: lsa object with all the cards encoding
    :param card_loader: loader with magic cards
    :return: hash with recommendations
    '''
    card_id = card_loader.hash_name_id[card_name]

    similarities = pd.DataFrame(columns=['card_id', 'content_similarity'])
    for i, new_card_id in enumerate(card_loader.hash_id_name.keys()):
        new_card = pd.DataFrame(index=[new_card_id], columns=['card_id', 'content_similarity'])
        new_card['content_similarity'] = lsa_manager.get_similarity(card_id, new_card_id)
        similarities = similarities.append(new_card)

    similarities = similarities.sort_values(['content_similarity'], ascending=[False])
    recommendations = {}
    nb = min(nb_recommendations, len(similarities))
    for i in range(nb):
        recommendations[card_loader.hash_id_name[similarities.index[i]]] = similarities.iloc[i]['content_similarity']

    with open('./../cntent_similarities_' + card_name.lower() + '.json', 'w') as f:
        json.dump(recommendations, f)

if __name__ == "__main__":
    print('Load magic environment')
    card_loader = load_magic_environment()

    print('Convert card text into vector')
    lsa_manager = encoding_magic_card(card_loader)
    #print_similarities(lsa_manager)

    print('Generate recommendations')
    print_similarities_card('Pia Nalaar', 6, lsa_manager, card_loader)
