# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Generate in Json format for each mode and colors:
# - Cards database (multiverseid, name, colors, type, LSA encoding)
# - Decks used for modelling
# - Top N Recommendation models
#

from pipeline.pipeline import Pipeline
from pipeline.pipeline import Model
from loader.utils import *
from lsa.lsa_encoder import LSAManager
import itertools

if __name__ == "__main__":
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)

    lsa_manager = LSAManager(card_loader.cards_multiverseid.values())
    lsa_manager.encode()

    pipeline = Pipeline()
    bpr_parameters = {'N': 5, 'lbd_I': 0.01, 'lbd_J': 0.005, 'learning_rate': 0.1, 'epoch': 200,
                      'batch_size': 100, 'decay': 0.5, 'nb_early_learning': 20, 'min_leaning_rate': 0.025,
                      'normalize': True}
    pipeline.add_model(Model.BPR_KNN, bpr_parameters)

    all_colors = [MagicLoader.CODE_BLUE, MagicLoader.CODE_BLACK, MagicLoader.CODE_GREEN, MagicLoader.CODE_RED, MagicLoader.CODE_WHITE]
    list_colors = []

    for nb_colors in range(1, 6):
        for combination in itertools.combinations(all_colors, nb_colors):
            code_color = 0
            for color in combination:
                code_color = code_color | color
            list_colors.append(code_color)
    list_colors.append(MagicLoader.CODE_NO_COLOR)
    list_modes = [MagicLoader.JSON_COMMANDER, MagicLoader.JSON_LEGACY, MagicLoader.JSON_MODERN, MagicLoader.JSON_PAUPER, MagicLoader.JSON_STANDARD, MagicLoader.JSON_VINTAGE]

    print("Generate catalogs")
    for color in list_colors:
        for mode in list_modes:
            if mode in decks_loader and color in  decks_loader[mode].grouped_decks:
                decks = decks_loader[mode].grouped_decks[color]
                card_catalog = generate_card_catalog(decks_loader, mode, color)
                dataset_name = mode + '_' + MagicLoader.get_json_color(color)
                pipeline.add_dataset(dataset_name, decks, card_catalog)

                lsa_manager.save(card_catalog, './resources', 'lsa_' + dataset_name)
                save_catalog(card_catalog, card_loader, 'catalog_' + dataset_name, './resources')
                save_decks(decks, 'decks_' + dataset_name, './resources')

    print("Start pipeline")
    pipeline.prepare()
    pipeline.build()
    pipeline.save('./resources')