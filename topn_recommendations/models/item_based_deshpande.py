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

        similarities = pd.Series(self.model.as_matrix().dot(deck.as_matrix()), index=self.card_catalog)
        for multiverseid in built_deck:
            similarities[multiverseid] = 0 #Avoid to recommend alreasdy selected cards

        n = min(n_recommendations, len(similarities))
        recommendations = similarities.nlargest(n)
        return recommendations[recommendations > 0.0]

    def compute_items_similarities(self, similarity_model, lsa_manager, alpha):
        item_recommender = ItemToItem(self.card_catalog)
        item_recommender.load_ratings(self.decks)
        item_recommender.compute_similarities(self.decks, similarity_model, lsa_manager, alpha)
        return item_recommender

    def save_coefficients(self, path):
        #self.model.to_json(path)
        self.model.to_pickle(path)

    @staticmethod
    def load_coefficients(path):
        #self.model = pd.read_json(path)
        df = pd.read_pickle(path)
        model = ItemBasedDeshpande(list(df.index), [])
        model.model = df
        return model