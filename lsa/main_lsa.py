import os
import json
from tqdm import tqdm
from loader_magic import MagicLoader, DeckManager
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

if __name__ == "__main__":
    print('Load magic environment')
    card_loader = load_magic_environment()

    print('Convert card text into vector')
    lsa_manager = encoding_magic_card(card_loader)

    lsa_manager.encoder.print_similarity()