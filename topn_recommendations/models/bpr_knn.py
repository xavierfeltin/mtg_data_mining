# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Bayesian Personal Ranking with KNN model
# Bibliogrpahy: https://arxiv.org/ftp/arxiv/papers/1205/1205.2618.pdf

import numpy as np
import pandas as pd
import math
from scipy.special import expit
from collections import deque, defaultdict

class BPRKNN:

    def __init__(self, card_catalog, decks):
        self.card_catalog = card_catalog
        self.decks = decks
        self.C = None
        self.gradientC = None
        self.momentum = defaultdict(float)
        self.learning_rate_0 = None
        self.learning_rate = None
        self.scores = deque()
        self.epoch = None
        self.ep = None
        self.last_evaluations = deque()
        self.n_eval = None

    def build_model(self, test_cards, N=5, lbd_I=0.05, lbd_J=0.01, learning_rate=0.01, epoch=30, batch_size=50, decay=0.5, nb_early_learning = 10, min_leaning_rate = 0.025):
        #print('Build models ...')
        self._init_coefficients()
        self.learning_rate_0 = learning_rate
        self.learning_rate = learning_rate
        self.epoch = epoch
        self.ep = 0
        self.n_eval = nb_early_learning

        #for ep in range(epoch):
        ep = 0
        while ep < epoch and self.learning_rate >= min_leaning_rate:

            #print('Epoch ' + str(ep) + ', learning rate: ' + str(self.learning_rate))
            self.ep = ep
            decks, items_i, items_j = self._get_sampling(batch_size)

            #update learning rate
            #learning_rate = self._step_decay(ep, decay, epochs_drop)
            #print('lr: ' + str(learning_rate))
            self._step_decay(decay)

            #print('Train...')
            for i in range(batch_size):
                self.gradientC = defaultdict(float)
                self._train(decks[i], items_i[i], items_j[i], lbd_I, lbd_J, self.learning_rate)

            evaluation = self._eval(test_cards, N)
            self.scores.append(evaluation)
            self._add_evaluations(evaluation)

            ep += 1

    def get_top_N_recommendations(self, built_deck, n_recommendations):
        '''
        Return the top N recommendations greater than 0 depending of the card selected in the deck passed in argument
        :param built_deck: deck being built by user
        :param n_recommendations: number of recommendations
        :return: list of items recommended
        '''

        deck = pd.Series(0, index=self.card_catalog)
        for multiverseid in built_deck:
            deck[multiverseid] = 1

        res = pd.Series(0.0, index=self.card_catalog)
        for i in self.C.index:
            res[i] = self.C[i].as_matrix().dot(deck.as_matrix())

        for i in built_deck:
            res[i] = 0.0

        recommendations = res.nlargest(n_recommendations)
        return recommendations[recommendations > 0.0]

    def _train(self, deck, item_i, item_j, lbd_I, lbd_J, learning_rate):
        '''
        Learn coefficients for C based on stochastic gradient descent
        :param deck: current deck processed
        :param item_i: item i in deck
        :param item_j: item j in deck
        '''

        x_di = sum([self.C.at[item_i,card] for card in deck if item_i != card])
        x_dj = sum([self.C.at[item_j,card] for card in deck if item_j != card])
        x_dij = x_di - x_dj

        for card in deck:
            if card != item_i:
                self.gradientC[(item_i, card)] += (1 - self.sigmoid(x_dij)) + lbd_I * self.C.at[item_i,card]
                self.gradientC[(card, item_i)] += (1 - self.sigmoid(x_dij)) + lbd_I * self.C.at[card,item_i]
            else:
                g = lbd_I * self.C.at[item_i, card]
                self.gradientC[(item_i, card)] += lbd_I * self.C.at[item_i,card]
                self.gradientC[(card, item_i)] += lbd_I * self.C.at[card,item_i]

            if card != item_j:
                self.gradientC[(item_j, card)] += -(1 - self.sigmoid(x_dij)) + lbd_J * self.C.at[item_j,card]
                self.gradientC[(card, item_j)] += -(1 - self.sigmoid(x_dij)) + lbd_J * self.C.at[card,item_j]
            else:
                g = lbd_J * self.C.at[item_j, card]
                self.gradientC[(item_j, card)] += lbd_J * self.C.at[item_j,card]
                self.gradientC[(card, item_j)] += lbd_J * self.C.at[card,item_j]

        for a, b in self.gradientC:
            self.C.at[a, b] += self._compute_momentum(a,b, learning_rate)

        self.prevGradientC = self.gradientC.copy()

    def _eval(self, test_cards, N):
        '''
        Compute DeltaC
        '''

        nb_hits = 0
        arhr = 0
        for i, deck in enumerate(self.decks):
            recommendations = self.get_top_N_recommendations(deck, N)
            if test_cards[i] in recommendations:
                position = recommendations.index.get_loc(test_cards[i]) + 1
                arhr += 1.0 / position
                nb_hits += 1
        hr = nb_hits / len(self.decks)
        arhr = arhr / len(self.decks)

        return (hr, arhr)


    def _init_coefficients(self):
        '''
        Initialize the model's coefficients
        '''

        #print('Init coefficients ...')

        self.C = pd.DataFrame(np.random.rand(len(self.card_catalog), len(self.card_catalog)), index=self.card_catalog, columns=self.card_catalog)
        for i, card in enumerate(self.card_catalog):
            # Diagonal at 0
            self.C.at[card, card] = 0.0

            # Set symetry
            for j in range(i + 1, len(self.card_catalog)):
                card_j = self.card_catalog[j]
                self.C.at[card_j, card] = self.C.at[card, card_j]

    def _get_sampling(self, batch_size):
        '''
        Return a random triplet of deck, card, card
        The random function is normally distributed
        :return: triplet (deck, card selected in deck, card not selected in deck)
        '''

        #print('Get samplings ...')

        samp_decks = deque()
        samp_items_i = deque()
        samp_items_j = deque()

        for _ in range(batch_size):
            index_deck = np.random.randint(0, len(self.decks))
            while len(self.decks[index_deck]) <= 1:
                index_deck = np.random.randint(0, len(self.decks))

            index_item_i = np.random.randint(0, len(self.decks[index_deck]))
            difference = list(frozenset(self.card_catalog).difference(self.decks[index_deck]))
            index_item_j = np.random.randint(0, len(difference))

            samp_decks.append(self.decks[index_deck])
            samp_items_i.append(self.decks[index_deck][index_item_i])
            samp_items_j.append(difference[index_item_j])

        return samp_decks, samp_items_i, samp_items_j


    def sigmoid(self, x):
        return expit(x)

    #def _step_decay(self, epoch, decay, epochs_drop):
    def _step_decay(self, decay):
        #lrate = self.learning_rate_0 * math.pow(decay, math.floor((1 + epoch) / epochs_drop))
        #return lrate

        if not self._is_still_learning():
            #print('Not learning anymore ...')
            self.learning_rate = self.learning_rate * decay
            self.last_evaluations.clear() #wait n epochs before reevaluating

    def get_scores(self):
        return self.scores

    def _compute_momentum(self, a, b, learning_rate):
        '''
        source: https://towardsdatascience.com/stochastic-gradient-descent-with-momentum-a84097641a5d
        :return: current momentum
        '''

        coefficient = 0.5

        momentum = 0.0
        if (a, b) in self.momentum:
            momentum = self.momentum[(a,b)]

        #self.momentum[(a,b)] = coefficient * momentum + (1.0-coefficient) * self.gradientC[(a,b)]
        #res = learning_rate *self.momentum[(a,b)]

        self.momentum[(a,b)] = coefficient * momentum + learning_rate * self.gradientC[(a,b)]
        res = self.momentum[(a,b)]

        return res

    def _add_evaluations(self, evaluation):
        if len(self.last_evaluations) >= self.n_eval:
            self.last_evaluations.popleft()

        self.last_evaluations.append(evaluation)

    def _is_still_learning(self):
        if len(self.last_evaluations) >= self.n_eval:
            current_hr, current_arhr, delta_hr, delta_arhr = 0, 0, 0, 0
            previous_hr = self.last_evaluations[self.n_eval - 1][0]
            previous_arhr = self.last_evaluations[self.n_eval - 1][1]
            for i in reversed(range(self.n_eval - 1)):
                current_hr, current_arhr = self.last_evaluations[i]
                delta_hr += (current_hr - previous_hr)
                delta_arhr += (current_arhr - previous_arhr)
                previous_hr = current_hr
                previous_arhr = current_arhr

            #print('delta: ' + str(abs(delta_hr)))
            #return abs(delta_hr) > 1e-6

            #print('delta: ' + str(abs(delta_hr + delta_arhr)))
            return abs(delta_hr + delta_arhr) > 0.001

        else:
            #print('delta: N/A')
            return True