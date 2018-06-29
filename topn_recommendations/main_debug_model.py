# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Main for building and saving models
#

from topn_recommendations.utils import *
from loader.magic_loader import MagicLoader
from topn_recommendations.models.bpr_knn import BPRKNN
from collections import deque
from time import time

if __name__ == "__main__":
    print('Load Magic environment')
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)

    studied_decks = {}
    decks_runs_random_items = {}

    mode = MagicLoader.JSON_COMMANDER
    # mode = MagicLoader.JSON_LEGACY

    color = MagicLoader.CODE_RED
    # color = MagicLoader.CODE_WHITE | MagicLoader.CODE_BLUE | MagicLoader.CODE_BLACK | MagicLoader.CODE_GREEN

    nb_runs = 1
    add_deck_serie(studied_decks, decks_runs_random_items, mode, color, decks_loader, nb_runs)
    card_catalog = generate_card_catalog(decks_loader, mode, color)

    start = time()
    #commander rouge: lbd_I=0.05, lbd_J=0.01
    #legacy 4 color: lbd_I=0.01, lbd_J=0.005

    scores = []
    scores_topN = []
    for i in range(nb_runs):
        print('run: ' + str(i))

        model = BPRKNN(card_catalog, studied_decks[mode][color][i], decks_runs_random_items[mode][color][i])
        model.build_model(N=5, lbd_I=0.01,
                          lbd_J=0.005, learning_rate=0.1, epoch=200, batch_size=100, decay=0.5, nb_early_learning=20,
                          min_leaning_rate=0.025)

        mod_scores = model.get_scores()
        scores.append(mod_scores[len(mod_scores)-1])
        print('internal: ' + str(mod_scores))

        nb_hits = 0
        arhr_score = 0
        for index, multiverseid_test in enumerate(decks_runs_random_items[mode][color][i]):
            recommendations = model.get_top_N_recommendations(studied_decks[mode][color][i][index], 5)

            if multiverseid_test in recommendations:
                position = recommendations.index.get_loc(multiverseid_test) + 1
                arhr_score += 1.0 / position
                nb_hits += 1
        hr = nb_hits / len(decks_runs_random_items[mode][color][i])
        arhr = arhr_score / len(decks_runs_random_items[mode][color][i])
        scores_topN.append((hr, arhr))
        print('top N: ' + str((hr, arhr)))

    print('time numpy: ' + str(round(time() - start, 4) * 1000))

    print('Evaluation synthesis from model:')
    HR = 0
    ARHR = 0
    for score in scores:
        HR += score[0]
        ARHR += score[1]
    print('HR: ' + str(HR/len(scores)) + '\t ARHR' + str(ARHR/len(scores)))

    print('Evaluation synthesis from top N recommendations:')
    HR = 0
    ARHR = 0
    for score in scores_topN:
        HR += score[0]
        ARHR += score[1]
    print('HR: ' + str(HR/len(scores_topN)) + '\t ARHR' + str(ARHR/len(scores_topN)))