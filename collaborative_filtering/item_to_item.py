import pandas as pd
import numpy as np
from collections import deque
from scipy import spatial
import math

#Bibliography
# - https://www.cs.umd.edu/~samir/498/Amazon-Recommendations.pdf
# - https://en.wikipedia.org/wiki/Item-item_collaborative_filtering

class Rating:
    def __init__(self, first_value, db_size = 0):
        self.first_value = first_value
        self.compression = deque()
        self.norm_square = 0
        self.db_size = db_size

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
            rating = Rating(current_value, db_size)

            start_index = 0
            for i, deck in enumerate(db):
                new_val = card in deck
                if new_val == current_value:
                    if new_val:
                        rating.norm_square += 1.0
                else:
                    current_value = new_val
                    if new_val:
                        start_index = i
                        rating.norm_square += 1.0
                    else:
                        rating.compression.append((start_index, i-1))

            if new_val:
                rating.compression.append((start_index, len(db)-1))

            rating.norm_square = math.sqrt(rating.norm_square)
            self.ratings[card] = rating

    def compute_similarities(self, db):
        '''
        Compute similarities between items
        '''

        df = pd.DataFrame(np.nan, index=self.catalog, columns=self.catalog)
        one_deck_db = len(db) == 1

        for item in self.catalog:
            if self.ratings[item].norm_square == 0.0:
                df.at[:, item] = -1.0
                df.at[item, :] = -1.0
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
                                        similarity = ItemToItem.compute_cosine_angle_binary(self.ratings[item], self.ratings[card])
                                        #similarity = ItemToItem.compute_cosine_angle(list_item, self.ratings[card].uncompress())

                                        if np.isnan(similarity):
                                            df.at[item, card] = -1.0
                                            df.at[card, item] = -1.0
                                        else:
                                            df.at[item, card] = similarity
                                            df.at[card, item] = similarity
                                    else:
                                        df.at[item, item] = -1.0
        self.items_similarities = df

    def get_recommendation(self, card_id, nb_recommendations, lsa):
        '''
        Return the list of the first nb_recommendations
        :param card_id: id card of which we want the recommendations
        :param nb_recommendations: number of recommendations to return
        :param lsa: language semantic analysis object from lsa package
        :return: dictionary {card_id: recommendation}
        '''

        item_similarities = self.items_similarities.loc[card_id]

        #Remove null or negative similarities
        item_similarities = item_similarities[item_similarities > 0].dropna()

        similarities = pd.DataFrame(columns=['card_id','item_similarity','content_similarity'])
        for i, new_card_id in enumerate(item_similarities.index):
            new_card = pd.DataFrame(index=[new_card_id], columns=['card_id','item_similarity','content_similarity'])
            new_card['item_similarity'] = item_similarities.loc[new_card_id]
            new_card['content_similarity'] = lsa.get_similarity(card_id, new_card_id)
            similarities = similarities.append(new_card)

        similarities = similarities.sort_values(['item_similarity', 'content_similarity'], ascending=[False, False])
        recommendations = {}
        nb = min(nb_recommendations, len(similarities))
        for i in range(nb):
            recommendations[similarities.index[i]] = [similarities.iloc[i]['item_similarity'],similarities.iloc[i]['content_similarity']]
        return recommendations

    @staticmethod
    def compute_cosine_angle(dataset_1, dataset_2):
        return 1.0 - spatial.distance.cosine(dataset_1, dataset_2)

    @staticmethod
    def compute_cosine_angle_binary(r1, r2):
        if r1.norm_square == 0 or r2.norm_square == 0: return np.nan

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
                i+=1

        return dot / (r1.norm_square * r2.norm_square)