# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Main for evaluating models using HR and ARHR indicators
# Statistics are based on paired t-tests
#


import os
from random import randint
from multiprocessing import Pool, Manager
from collections import deque
import xlsxwriter
from numpy import isnan

from loader.magic_loader import MagicLoader
from loader.deck_manager import DeckManager
from collaborative_filtering.item_to_item import ItemToItem
from topn_recommendations.models.item_based_deshpande import ItemBasedDeshpande
from topn_recommendations.models.utils import ModelParameters, ModelResults, KeyGenerator
from lsa.lsa_encoder import LSAManager
from stats.statistic_results import StatisticResults, ConsolidateResults

def load_magic_environment():
    print('Load magic environment')
    card_loader = MagicLoader()
    card_loader.load_from_set('./../data/magic_cards/AllSets-x.json')
    return card_loader

def load_decks(card_loader):
    print('Load decks')

    files = os.listdir("./../data/decks_mtgdeck_net_extended")  # returns list
    paths = []
    for file in files:
        paths.append('./../data/decks_mtgdeck_net_extended/' + file)

    decks = {}
    for mode in MagicLoader.HASH_GAME_STRING_CODE.keys():
        for path in paths:
            if mode.lower() in path:
                deck_loader = DeckManager()
                deck_loader.load_from_mtgdeck_csv([path], cards_loader=card_loader, ignore_land=True)
                deck_loader.sort_decks()
                decks[mode] = deck_loader

    return decks

def get_cards_from_decks(decks_loader, card_loader):
    multiverseid_in_decks = set()
    for mode in decks_loader:
        multiverseid_in_decks = multiverseid_in_decks.union(decks_loader[mode].cards)
    list_multiverseid_in_decks = list(multiverseid_in_decks)
    cards_in_decks = card_loader.extract_cards(list_multiverseid_in_decks)
    return cards_in_decks

def encoding_magic_card_subsets(cards):
    hash_id_texts = {}
    for card in cards:
        hash_id_texts[card.multiverseid] = card.full_text

    lsa_manager = LSAManager(hash_id_texts)
    lsa_manager.encode()
    return lsa_manager

def test_model(k_neighbors,n_recommendations, decks, random_items, alpha, norm_sim, model_sim,lsa_manager):
    '''
    Build training and test sets
    Take randomly one card from each deck and then use the rest of the decks for training
    :param k_neighbors:
    :param n_recommendations:
    :param decks:
    :param random_items:
    :param alpha:
    :param norm_sim:
    :param model_sim:
    :param lsa_manager:
    :return: tuple with hr scoore and arhr scoreof the model
    '''

    training_set = deque()
    all_catalog = deque()
    testing_set = deque()
    for i, deck in enumerate(decks):
        rand_index = random_items[i]
        training_deck = deck[:]
        del training_deck[rand_index]
        training_set.append(training_deck)
        testing_set.append(deck[rand_index])
        all_catalog.extend(training_deck)
    training_catalog = deque()
    training_catalog.extend(list(set(all_catalog)))

    # Process red colored decks only on training set
    modelTopN = ItemBasedDeshpande(training_catalog, training_set)
    if model_sim == ModelParameters.MODEL_SIM_COSINE:
        model_similarities = ItemToItem.compute_cosine_angle_binary
    elif model_sim == ModelParameters.MODEL_SIM_COSINE_LSA:
        model_similarities = ItemToItem.compute_cosine_angle_binary_lsa
    elif model_sim == ModelParameters.MODEL_SIM_COSINE_ROW:
        model_similarities = ItemToItem.compute_cosine_angle_binary_row
    elif model_sim == ModelParameters.MODEL_SIM_COSINE_LSA_ROW:
        model_similarities = ItemToItem.compute_cosine_angle_binary_lsa_row
    else:
        model_similarities = ItemToItem.compute_probability

    modelTopN.build_model(k_neighbors, model_similarities, lsa_manager, alpha, normalize_similarities=norm_sim)

    nb_hits = 0
    arhr_score = 0
    for index, multiverseid_test in enumerate(testing_set):
        recommendations = modelTopN.get_top_N_recommendations(training_set[index], n_recommendations)

        if multiverseid_test in recommendations:
            position = recommendations.index.get_loc(multiverseid_test) + 1
            arhr_score += 1.0 / position
            nb_hits += 1

    hr_score = nb_hits / len(testing_set)
    arhr_score = arhr_score / len(testing_set)
    return (hr_score, arhr_score)

def worker(id, jobs_queue, results_queue):
    while True:
        data = jobs_queue.get()
        if data is None:
            return 0

        print('idRun: ' + str(data.id_run) + ', k:' + str(data.k) + ', color:'
              + str(MagicLoader.get_json_color(data.color)) + ', nb decks: ' + str(len(data.decks)))

        scores = test_model(data.k, data.n, data.decks, data.random_items, data.alpha, data.norm_sim, data.similarity_model, data.lsa_manager)
        result = ModelResults(data.id_run, data.k, data.mode, data.color, scores)
        results_queue.put(result)

def process_recommendations(nb_run, k_min, k_max, n, decks, decks_random_items_run, alpha, norm_sim, model_sim, lsa_manager):
    '''
    Producer / Consumer model for multithreading
    :param: hash of decks grouped by game mode
    :return: queue with the results
    '''

    tests_to_process = deque()
    for r in range(nb_runs):
        for mode in decks:
            for color in decks[mode]:
                for k in range(k_min, k_max):
                    tests_to_process.append(ModelParameters(r, k, n, decks[mode][color], decks_random_items_run[mode][color][r], mode, color, alpha, norm_sim, model_sim, lsa_manager))

    number_wokers = 6
    manager = Manager()
    pool = Pool(processes=number_wokers)
    jobs_queue = manager.Queue()
    results_queue = manager.Queue()

    for testParameters in tests_to_process:
        jobs_queue.put(testParameters)

    # stop workers
    for i in range(number_wokers):
        jobs_queue.put(None)

    for i in range(number_wokers):
        results = pool.apply_async(worker, (i, jobs_queue, results_queue))

    pool.close()
    pool.join()

    return results_queue

def generate_excel_array_results(worksheet, row_id, statistics):
    for s in statistics:
        if s is None:
            print('S is None !')

        rejected = s.reject_null_hypothesis(0.95)
        ttests = s.compute_pairedttest()
        confidence_intervals = s.compute_confidence_interval(0.95)
        means = s.get_means()

        worksheet.write_row(row_id, 1, [s.title])
        row_id += 1
        columns_names = ['Group 1', 'Group 2', 'Mean 1', 'Mean 2', 'Mean Diff', 'Lower', 'Upper', 'p-value', 'Reject?']
        worksheet.write_row(row_id, 1, columns_names)
        row_id += 1
        for index, pair in enumerate(s.generator_pairs()):
            x, y = pair

            p_value = ttests[index][1]
            if isnan(p_value):
                p_value = 'nan'

            diff_mean = confidence_intervals[index][0]
            if isnan(diff_mean):
                diff_mean= 'nan'
            else:
                diff_mean = round(diff_mean, 3)

            lower = confidence_intervals[index][1]
            if isnan(lower):
                lower= 'nan'
            else:
                lower = round(lower, 3)

            upper = confidence_intervals[index][2]
            if isnan(upper):
                upper = 'nan'
            else:
                upper = round(lower, 3)


            data = [s.subtitles[x], s.subtitles[y], round(means[x], 3), round(means[y], 3), diff_mean, lower, upper,
                    p_value, str(rejected[index])]
            worksheet.write_row(row_id, 1, data)
            row_id += 1

        row_id += 1
    return row_id

def generate_excel_results(filename, nb_runs, k, statistics_HR, statistics_ARHR):
    workbook = xlsxwriter.Workbook(filename + '.xlsx')
    worksheet = workbook.add_worksheet('HR_ARHR')

    titles = ['HR scores']
    worksheet.write_row(1, 1, titles)
    last_row_id = generate_excel_array_results(worksheet, 2, statistics_HR)

    titles = ['ARHR scores']
    worksheet.write_row(last_row_id + 2, 1, titles)
    last_row_id = generate_excel_array_results(worksheet, last_row_id + 3, statistics_ARHR)

    workbook.close()

def modelisation_multi_process(nb_run, k_min, k_max, n_recommendations, alpha, norm_sim, model_sim, studied_decks, decks_runs_random_items, lsa_manager):
    results_queue = process_recommendations(nb_run, k_min, k_max, n_recommendations, studied_decks, decks_runs_random_items, alpha, norm_sim, model_sim, lsa_manager)
    results = {}
    while not results_queue.empty():
        model_score = results_queue.get()
        key = KeyGenerator.getKeyFromModelResults(model_score)
        results[key] = model_score.results
    return results

def prepare_deck_data(decks_loader, mode, color, nb_runs):
    decks_to_prepare = decks_loader[mode].grouped_decks[color]
    runs_random_items = []
    for i in range(nb_runs):
        random_items = []
        for deck in decks_to_prepare:
            random_items.append(randint(0, len(deck) - 1))
        runs_random_items.append(random_items)
    return decks_to_prepare, runs_random_items

if __name__ == "__main__":
    print('Load Magic environment')
    card_loader = load_magic_environment()
    decks_loader = load_decks(card_loader)
    lsa_manager = encoding_magic_card_subsets(get_cards_from_decks(decks_loader, card_loader))

    print('Preparing evaluations...')
    studied_decks = {}
    studied_decks[MagicLoader.JSON_COMMANDER] = {}
    studied_decks[MagicLoader.JSON_LEGACY] = {}
    studied_decks[MagicLoader.JSON_PAUPER] = {}
    decks_runs_random_items = {}
    decks_runs_random_items[MagicLoader.JSON_COMMANDER] = {}
    decks_runs_random_items[MagicLoader.JSON_LEGACY] = {}
    decks_runs_random_items[MagicLoader.JSON_PAUPER] = {}

    nb_runs = 20
    k_min = 13
    k_max = 14
    n_recommendations = 5
    alpha = 0.5

    # 1 color
    studied_decks[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED], decks_runs_random_items[MagicLoader.JSON_COMMANDER][MagicLoader.CODE_RED] = \
        prepare_deck_data(decks_loader, MagicLoader.JSON_COMMANDER, MagicLoader.CODE_RED, nb_runs)
    studied_decks[MagicLoader.JSON_PAUPER][MagicLoader.CODE_RED], decks_runs_random_items[MagicLoader.JSON_PAUPER][MagicLoader.CODE_RED] = \
        prepare_deck_data(decks_loader, MagicLoader.JSON_PAUPER, MagicLoader.CODE_RED, nb_runs)

    # 3 colors
    black_blue_red = MagicLoader.CODE_RED | MagicLoader.CODE_BLUE | MagicLoader.CODE_BLACK
    studied_decks[MagicLoader.JSON_COMMANDER][black_blue_red], decks_runs_random_items[MagicLoader.JSON_COMMANDER][black_blue_red] \
        = prepare_deck_data(decks_loader, MagicLoader.JSON_COMMANDER, black_blue_red, nb_runs)
    studied_decks[MagicLoader.JSON_LEGACY][black_blue_red], decks_runs_random_items[MagicLoader.JSON_LEGACY][black_blue_red] \
        = prepare_deck_data(decks_loader, MagicLoader.JSON_LEGACY, black_blue_red, nb_runs)

    # 4 colors
    black_blue_green_white = MagicLoader.CODE_WHITE | MagicLoader.CODE_BLUE | MagicLoader.CODE_BLACK | MagicLoader.CODE_GREEN
    studied_decks[MagicLoader.JSON_COMMANDER][black_blue_green_white], decks_runs_random_items[MagicLoader.JSON_COMMANDER][black_blue_green_white] \
        = prepare_deck_data(decks_loader, MagicLoader.JSON_COMMANDER, black_blue_green_white, nb_runs)
    studied_decks[MagicLoader.JSON_LEGACY][black_blue_green_white], decks_runs_random_items[MagicLoader.JSON_LEGACY][black_blue_green_white] \
        = prepare_deck_data(decks_loader, MagicLoader.JSON_LEGACY, black_blue_green_white, nb_runs)

    # 5 colors
    five_colors = MagicLoader.CODE_RED | MagicLoader.CODE_BLUE | MagicLoader.CODE_BLACK | MagicLoader.CODE_WHITE | MagicLoader.CODE_GREEN
    studied_decks[MagicLoader.JSON_LEGACY][five_colors], decks_runs_random_items[MagicLoader.JSON_LEGACY][five_colors] \
        = prepare_deck_data(decks_loader, MagicLoader.JSON_LEGACY, five_colors, nb_runs)
    studied_decks[MagicLoader.JSON_PAUPER][five_colors], decks_runs_random_items[MagicLoader.JSON_PAUPER][five_colors] \
        = prepare_deck_data(decks_loader, MagicLoader.JSON_PAUPER, five_colors, nb_runs)

    #modelisation_single_process(nb_run,k_min,k_max,n_recommendations)
    results = deque()
    subtitles = deque()
    model_type = 'simu_cosine'

    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, False, ModelParameters.MODEL_SIM_COSINE,studied_decks, decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, True, ModelParameters.MODEL_SIM_COSINE, studied_decks, decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, True, ModelParameters.MODEL_SIM_COSINE_ROW,studied_decks, decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, False,ModelParameters.MODEL_SIM_COSINE_LSA, studied_decks,decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, True, ModelParameters.MODEL_SIM_COSINE_LSA,studied_decks, decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, True, ModelParameters.MODEL_SIM_COSINE_LSA_ROW,studied_decks, decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, False, ModelParameters.MODEL_SIM_PROBA,studied_decks, decks_runs_random_items, lsa_manager))
    results.append(modelisation_multi_process(nb_runs, 25, 26, n_recommendations, alpha, True,ModelParameters.MODEL_SIM_PROBA, studied_decks, decks_runs_random_items, lsa_manager))

    subtitles.append('cosine(-) 25k')
    subtitles.append('cosine(+) 25k')
    subtitles.append('cosine(+, row) 25k')
    subtitles.append('cosine lsa(-) 25k')
    subtitles.append('cosine lsa(+) 25k')
    subtitles.append('cosine lsa(+, row) 25k')
    subtitles.append('proba(-) 25k')
    subtitles.append('proba(+) 25k')

    print('Start consolidation and export statistics to excel')
    consolidated_results = deque()
    for result in results:
        consolidate = ConsolidateResults()
        for key, value in result.items():
            consolidate.add_result(key, value)
        consolidated_results.append(consolidate)

    statistics_HR = []
    statistics_ARHR = []
    for mode in consolidated_results[0].get_modes():
        for color in consolidated_results[0].get_colors(mode):
            stat_HR_results = StatisticResults('HR - ' + mode + ' ' + MagicLoader.get_json_color(color))
            stat_ARHR_results = StatisticResults('ARHR - ' + mode + ' ' + MagicLoader.get_json_color(color))
            for i, consolidated in enumerate(consolidated_results):
                stat_HR_results.add_series(consolidated.get_runs(mode, color, ConsolidateResults.HR), subtitles[i])
                stat_ARHR_results.add_series(consolidated.get_runs(mode, color, ConsolidateResults.ARHR),subtitles[i])
            statistics_HR.append(stat_HR_results)
            statistics_ARHR.append(stat_ARHR_results)

    generate_excel_results('./model_evaluation_results', nb_runs, k_min, statistics_HR, statistics_ARHR)