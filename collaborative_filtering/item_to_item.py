# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
#
# Bibliography
# - https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
# - https://en.wikipedia.org/wiki/Item-item_collaborative_filtering
#

import pandas as pd
import numpy as np
from collections import deque
from scipy import spatial
import math
from tqdm import tqdm


class Rating:
    def __init__(self, first_value, card, db_size = 0):
        self.first_value = first_value
        self.compression = deque()
        self.norm_square = 0
        self.frequency = 0
        self.db_size = db_size
        self.norm_square_normalized = 0
        self.card = card

    def uncompress(self):
        full_data = deque()
        index = 0
        for data in self.compression:
            start_index = data[0]
            end_index = data[1]

            full_data.extend([0] * (start_index - index))
            full_data.extend([1] * ((end_index + 1) - start_index))
            index = end_index + 1

        if index < self.db_size:
            full_data.extend([0] * (self.db_size - index))

        return full_data

class ItemToItem:
    def __init__(self, catalog_items):
        self.catalog = catalog_items
        self.items_ratings = pd.DataFrame()
        self.items_similarities = pd.DataFrame()
        self.ratings = {}

    def load_ratings(self, db):
        '''
        For each item generates a vector containing 1 if the card is chosen in the deck, 0 if not
        :param db: database containing all decks
        '''

        self.ratings.clear()
        db_size = len(db)
        for card in self.catalog:
            current_value = card in db[0]
            rating = Rating(current_value, card, db_size)

            start_index = 0
            for i, deck in enumerate(db):
                new_val = card in deck
                if new_val == current_value:
                    if new_val:
                        rating.norm_square += 1.0
                        rating.norm_square_normalized += 1.0/len(db)
                else:
                    current_value = new_val
                    if new_val:
                        start_index = i
                        rating.norm_square += 1.0
                        rating.norm_square_normalized += 1.0 / len(db)
                    else:
                        rating.compression.append((start_index, i-1))

            if new_val:
                rating.compression.append((start_index, len(db)-1))

            rating.frequency = rating.norm_square #for binary values only
            rating.norm_square = math.sqrt(rating.norm_square)
            rating.norm_square_normalized = math.sqrt(rating.norm_square_normalized)
            self.ratings[card] = rating

    def compute_similarities(self, db, similarity_model, lsa_manager, alpha=0.5):
        '''
        Compute similarities between items
        '''

        df = pd.DataFrame(np.nan, index=self.catalog, columns=self.catalog)
        one_deck_db = len(db) == 1

        for item in self.catalog:
            if self.ratings[item].norm_square == 0.0:
                df.at[:, item] = 0.0
                df.at[item, :] = 0.0
            else:
                if one_deck_db:
                    for card in db[0]:
                        if card != item:
                            df.at[item, card] = 1.0
                            df.at[card, item] = 1.0
                else:
                    #list_item = self.ratings[item].uncompress()

                    for start_end in self.ratings[item].compression:
                        for j in range(start_end[0], start_end[1]+1):
                            for card in db[j]:
                                if np.isnan(df.at[card, item]):
                                    if card != item:
                                        similarity = similarity_model(self.ratings[item], self.ratings[card], lsa_manager, alpha, db)
                                        #similarity = ItemToItem.compute_cosine_angle_binary(self.ratings[item], self.ratings[card])
                                        #similarity = ItemToItem.compute_cosine_angle(list_item, self.ratings[card].uncompress())

                                        if np.isnan(similarity):
                                            df.at[item, card] = 0.0
                                            df.at[card, item] = 0.0
                                        else:
                                            df.at[item, card] = similarity
                                            df.at[card, item] = similarity
                                    else:
                                        df.at[item, item] = 0.0
        self.items_similarities = df

    @staticmethod
    def compute_cosine_angle(dataset_1, dataset_2, alpha=0.0):
        return 1.0 - spatial.distance.cosine(dataset_1, dataset_2)

    @staticmethod
    def compute_cosine_angle_binary(r1, r2, lsa_manager, alpha=0.0, db = None):
        if r1.norm_square == 0 or r2.norm_square == 0: return np.nan
        #for binary values, dot products is similar to r1 intersect r2
        return ItemToItem._compute_r1_inter_r2_binary(r1,r2) / (r1.norm_square * r2.norm_square)

    def compute_cosine_angle_binary_lsa(r1, r2, lsa_manager, alpha=0.5, db = None):
        if r1.norm_square == 0 or r2.norm_square == 0: return np.nan
        lsa = lsa_manager.get_similarity(r1.card, r2.card)
        lsa = (((lsa + 1.0) / 2.0) * (1.0 - alpha)) + alpha #-1 => alpha, 1 => 1
        return (lsa * ItemToItem._compute_r1_inter_r2_binary(r1,r2)) / (r1.norm_square * r2.norm_square)

    @staticmethod
    def compute_cosine_angle_binary_row(r1, r2, lsa_manager, alpha=0.0, db=None):
        if r1.norm_square == 0 or r2.norm_square == 0: return np.nan

        common_decks = ItemToItem._get_common_decks(r1, r2)
        sum = 0
        for common in common_decks:
            for i in range(common[0], common[1]):
                sum += pow(1.0 / len(db[i]),2)

        # for binary values, dot products is similar to r1 intersect r2
        return sum / (r1.norm_square * r2.norm_square)

    def compute_cosine_angle_binary_lsa_row(r1, r2, lsa_manager, alpha=0.5, db=None):
        if r1.norm_square == 0 or r2.norm_square == 0: return np.nan

        common_decks = ItemToItem._get_common_decks(r1, r2)
        sum = 0
        for common in common_decks:
            for i in range(common[0], common[1]):
                sum += pow(1.0 / len(db[i]), 2)

        lsa = lsa_manager.get_similarity(r1.card, r2.card)
        lsa = (((lsa + 1.0) / 2.0) * (1.0 - alpha)) + alpha  # -1 => alpha, 1 => 1
        return (lsa * sum) / (r1.norm_square * r2.norm_square)

    @staticmethod
    def compute_probability(r1, r2, lsa_manager, alpha=0.5, db = None):
        common_decks = ItemToItem._get_common_decks(r1, r2)
        sum = 0
        for common in common_decks:
            for i in range(common[0], common[1]):
                sum += 1.0 / len(db[i])
        return sum / (r1.frequency * pow(r2.frequency, alpha))

    @staticmethod
    def _compute_r1_inter_r2_binary(r1,r2):
        dot = 0
        len_r2 = len(r2.compression)
        i = 0
        for r1_start, r1_end in r1.compression:
            while i < len_r2 and r2.compression[i][1] <= r1_end:
                r2_start, r2_end = r2.compression[i]

                if r2_start < r1_start:
                    if r2_end >= r1_start and r2_end < r1_end:
                        dot += (r2_end + 1) - r1_start
                    elif r2_end > r1_end:
                        dot += (r1_end + 1) - r1_start
                elif r2_start >= r1_start:
                    if r2_end < r1_end:
                        dot += (r2_end + 1) - r2_start
                    elif r2_end >= r1_end:
                        dot += (r1_end + 1) - r2_start
                i += 1
        return dot

    @staticmethod
    def _get_common_decks(r1,r2):
        '''
        Return the list of common decks
        :return: list of indexes pairs (begin, end) of common decks
        '''
        common_decks = deque()
        len_r2 = len(r2.compression)
        i = 0
        for r1_start, r1_end in r1.compression:
            while i < len_r2 and r2.compression[i][1] <= r1_end:
                r2_start, r2_end = r2.compression[i]

                if r2_start < r1_start:
                    if r2_end >= r1_start and r2_end < r1_end:
                        common_decks.append((r1_start, (r2_end + 1)))
                    elif r2_end > r1_end:
                        common_decks.append((r1_start, (r1_end + 1)))
                elif r2_start >= r1_start:
                    if r2_end < r1_end:
                        common_decks.append((r2_start, (r2_end + 1)))
                    elif r2_end >= r1_end:
                        common_decks.append((r2_start, (r1_end + 1)))
                i += 1
        return common_decks