# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH

import numpy as np
import pandas as pd
from collaborative_filtering.item_to_item import ItemToItem

class ItemBasedDeshpande:
    '''
    Model to determine top N recommendations based on collaborative filtering item to item approach
    Bibliography:
    Item-Based Top-N Recommendation Algorithms, Mukund Deshpande and George Karypis,
    ACM Transactions on Information Systems. Volume 22, Issue 1, pp. 143 - 177, 2004
    http://glaros.dtc.umn.edu/gkhome/node/127 (https://dl.acm.org/citation.cfm?id=963776)
    '''

    def __init__(self, card_catalog, decks):
        self.card_catalog = card_catalog
        self.decks = decks
        self.model = None

    def build(self, parameters):
        self.build_model(k_neighbors=parameters['k_neighbors'], similarity_model=parameters['similarity_model'], lsa_manager=parameters['lsa_manager'],
                         alpha=parameters['alpha'], normalize_similarities=parameters['normalize_similarities'],
                         recommender=parameters['recommender'])

    def build_model(self, k_neighbors, similarity_model, lsa_manager, alpha = 0.5, normalize_similarities = False, recommender=None):
        '''
        Get the similarities from the item manager and force values lower than the last k values to 0
        replace nan values by 0 (non correlated items)
        :param k_neighbors: k best similarities kept for model
        '''

        if recommender is None:
            recommender = self.compute_items_similarities(similarity_model, lsa_manager, alpha)

        if normalize_similarities:
            similarities = recommender.items_similarities.copy()
            for column in similarities.index:
                sum = similarities[column].sum()
                similarities[column] = similarities[column].divide(sum)
        else:
            similarities = recommender.items_similarities

        self.model = similarities
        for item in self.model.index:
            max_k_values = self.model[item].nlargest(k_neighbors)
            mask = self.model[item] < max_k_values.min()
            self.model.loc[mask, item] = 0
        self.model.replace(np.nan,0,True)

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

        #similarities = pd.Series(self.model.as_matrix().dot(deck.as_matrix()), index=self.card_catalog)
        similarities = pd.Series(self.model.values.dot(deck.values), index=self.card_catalog)
        for multiverseid in built_deck:
            similarities[multiverseid] = 0 #Avoid to recommend alreasdy selected cards

        n = min(n_recommendations, len(similarities))
        recommendations = similarities.nlargest(n)
        return recommendations[recommendations > 0.0]

    def get_contributions(self, recommendations, built_deck, thresold=None, max_contributors = 5):
        contribution = {}

        if thresold is None:
            thresold = 1.0/len(built_deck)

        matrix_contributions = np.zeros((len(recommendations), len(built_deck)), dtype=np.float64)
        for i, rec_card in enumerate(recommendations):
            sum = 0.0
            for j, built_card in enumerate(built_deck):
                matrix_contributions[i][j] = self.model.at[rec_card, built_card]
                sum += self.model.at[rec_card, built_card]

            matrix_contributions[i] = matrix_contributions[i] / sum
            indexes = matrix_contributions[i].argsort()[::-1]

            relevant_cards = [(built_deck[x], matrix_contributions[i][x]) for x in indexes if matrix_contributions[i][x] > thresold]
            contribution[rec_card] = relevant_cards[0:max_contributors]
        return contribution

    def compute_items_similarities(self, similarity_model, lsa_manager, alpha):
        item_recommender = ItemToItem(self.card_catalog)
        item_recommender.load_ratings(self.decks)
        item_recommender.compute_similarities(self.decks, similarity_model, lsa_manager, alpha)
        return item_recommender

    def save_coefficients(self, path):
        #self.model.to_json(path)
        self.model.to_pickle(path)

    def get_name(self):
        return 'itemknn'

    @staticmethod
    def load_coefficients(path):
        #self.model = pd.read_json(path)
        df = pd.read_pickle(path)
        model = ItemBasedDeshpande(list(df.index), [])
        model.model = df
        return model

    @staticmethod
    def get_default_parameters():
        return {'k_neighbors':10, 'similarity_model':None, 'lsa_manager':None,
                'alpha':0.5, 'normalize_similarities':False, 'recommender':None}