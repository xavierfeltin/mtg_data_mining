import pandas as pd
import numpy as np
from collections import deque
from scipy import spatial
from tqdm import tqdm
from time import time

class Rating:
    def __init__(self, first_value):
        self.first_value = first_value
        self.compression = []
        self.norm_square = 0

    def uncompress(self):
        full_data = deque()
        current_value = self.first_value
        for data in self.compression:
            full_data.extend([current_value] * data)
            current_value = 1.0 - current_value
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

        '''
        ratings = deque()
        labels = range(len(db))
        for item in self.catalog:
            rating = deque()
            for j, deck in enumerate(db):
                rating.append(int(item in deck))
            ratings.append(rating)
        self.items_ratings = pd.DataFrame.from_records(ratings, index=self.catalog)
        '''

        self.ratings.clear()
        for card in tqdm(self.catalog):
            current_value = int(card in db[0])
            rating = Rating(current_value)
            nb_values = 0
            for deck in db:
                new_val = int(card in deck)
                if new_val == current_value:
                    nb_values += 1
                else:
                    rating.compression.append(nb_values)
                    nb_values = 1
                    current_value = new_val

                if new_val:
                    self.norm_square += 1

            rating.compression.append(nb_values)
            self.ratings[card] = rating

    def compute_similarities(self, db):
        '''
        Compute similarities between items
        '''

        database = db[:]
        df = pd.DataFrame(np.nan, index=self.catalog, columns=self.catalog)

        for item in tqdm(self.catalog):
            #list_item = self.items_ratings.loc[item].tolist()
            list_item = self.ratings[item].uncompress()
            if sum(list_item) == 0:
                df.at[:, item] = -1.0
                df.at[item, :] = -1.0
            else:
                for j, is_present in enumerate(list_item):
                    if is_present:
                        deck = database[j]
                        for card in deck:
                            if np.isnan(df.at[card, item]):
                                if card != item:
                                    similarity = self.compute_cosine_angle(list_item, self.ratings[card].uncompress())
                                    if np.isnan(similarity):
                                        df.at[item, card] = -1.0
                                        df.at[card, item] = -1.0
                                    else:
                                        df.at[item, card] = similarity
                                        df.at[card, item] = similarity
                                else:
                                    df.at[item, item] = -1.0
                        #deck.remove(item)
        self.items_similarities = df

    def get_recommendation(self, card_id, nb_recommendations, lsa):
        '''
        Return the list of the first nb_recommendations
        :param card_id: id card of which we want the recommendations
        :param nb_recommendations: number of recommendations to return
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

    def compute_cosine_angle(self, dataset_1, dataset_2):
        return 1.0 - spatial.distance.cosine(dataset_1, dataset_2)
        #TODO: ||v|| = sum(vector) because only 0 and 1 => precompute if need be
        #TODO: v1.v2 = AND logic between v1 and v2 then SUM of result because only 0 and 1
        #Try to work with ndarray and logical_and function from numpy