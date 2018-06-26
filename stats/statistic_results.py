# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH

from collections import deque
from topn_recommendations.models.utils import KeyGenerator
from stats.paired_t_test import PairedTTest

from numpy import average

class Results:
    def __init__(self):
        self.modes = deque()
        self.colors = {}

    def get_modes(self):
        return self.modes

    def get_colors(self, mode):
        return self.colors[mode]

class ConsolidateResults(Results):
    HR = 0
    ARHR = 1

    def __init__(self):
        Results.__init__(self)
        self.dict_hr = {}
        self.dict_arhr = {}

    def add_result(self, key, result):
        #id_run, k, mode, color = KeyGenerator.getElements(key)
        id_run, mode, color = KeyGenerator.getElements(key)
        id_run = int(id_run)
        color = int(color)
        #k = int(k)

        if mode not in self.modes:
            self.modes.append(mode)
            self.colors[mode] = deque()
            self.dict_hr[mode] = {}
            self.dict_arhr[mode] = {}

        if color not in self.colors[mode]:
            self.colors[mode].append(color)
            self.dict_hr[mode][color] = {}
            self.dict_arhr[mode][color] = {}

        self.dict_hr[mode][color][id_run] = result[0]
        self.dict_arhr[mode][color][id_run] = result[1]

    def get_nb_results(self, mode, color):
        return len(self.dict_hr[mode][color])

    def get_runs(self, mode, color, data_type):
        runs = deque()
        for i in range(self.get_nb_results(mode, color)):
            if data_type == ConsolidateResults.HR:
                runs.append(self.dict_hr[mode][color][i])
            else:
                runs.append(self.dict_arhr[mode][color][i])
        return runs

class StatisticResults(Results):
    def __init__(self, title):
        Results.__init__(self)
        self.title = title
        self.series = deque()
        self.subtitles = deque()
        self.ttests = None
        self.confidence_intervals = None
        self.rejections = None

    def clean_previous_analysis(self):
        self.ttests = None
        self.confidence_intervals = None
        self.rejections = None

    def add_series(self, serie, title):
        self.subtitles.append(title)
        self.series.append(serie)
        self.clean_previous_analysis()

    def clean_series(self):
        self.series.clear()
        self.clean_previous_analysis()

    def compute_pairedttest(self):
        if self.ttests is None:
            self.ttests = deque()
            for i, j in self.generator_pairs():
                self.ttests.append(PairedTTest.get_results(self.series[i], self.series[j]))
        return self.ttests

    def compute_confidence_interval(self, threshold=0.95):
        if self.confidence_intervals is None:
            self.confidence_intervals = deque()
            for i, j in self.generator_pairs():
                self.confidence_intervals.append(PairedTTest.get_confidence_interval(self.series[i], self.series[j], threshold))
        return self.confidence_intervals

    def get_means(self):
        means = deque()
        for serie in self.series:
            means.append(average(serie))
        return means

    def reject_null_hypothesis(self, alpha=0.95):
        '''
        Return an array of boolean indicating if the null hypothesis should be rejected.
        Alpha is adjusted with the Bonferroni correction (divided by the number of p-values)
        :param alpha: significance
        :return: array of boolean, True if the null hypothesis should be rejected
        '''
        if self.rejections is None:
            self.rejections = deque()
            if self.ttests is None:
                self.compute_pairedttest()

            significance = (1.0 - alpha) / len(self.ttests)

            for ttest in self.ttests:
                self.rejections.append(ttest[1] <= significance)
        return self.rejections

    def generator_pairs(self):
        for i in range(len(self.series) - 1):
            for j in range(i + 1, len(self.series)):
                yield (i, j)