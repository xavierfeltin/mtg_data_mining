# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH

from scipy import stats
from numpy import average, std, subtract
from math import sqrt

class PairedTTest:
    """
    Utils class to compute paired t-test on data series
    """

    @staticmethod
    def get_results(serie_1, serie_2):
        """
        Return t-statistics and p-value on two related samples
        serie_1 and serie_2 must have the same shape
        :param serie_1: serie of data
        :param serie_2: serie of data
        :return: tuple(t-statistics, p-value)
        """
        return stats.ttest_rel(serie_1, serie_2)

    @staticmethod
    def get_confidence_interval(serie_1, serie_2, confidence_threshold=0.95):
        """
        Return the difference mean between serie_1 and serie_2
        and associated confidence interval
        serie_1 and serie_2 must have the same shape
        :param serie_1: serie of data
        :param serie_2: serie of data
        :param conficende_threshold: confidence thresold
        :return: tuple (difference mean, interval_min, interval_max)
        """

        diff_serie = subtract(serie_1, serie_2)
        diff_mean = average(diff_serie)
        df = len(serie_1) - 1 #degree of freedom of two related samples
        std_dev = std(diff_serie, ddof=1)
        std_err = std_dev/sqrt(len(diff_serie))
        t_value_thresold = abs(stats.t.interval(confidence_threshold, df)[0])
        return (diff_mean, diff_mean - t_value_thresold * std_err, diff_mean + t_value_thresold * std_err)

