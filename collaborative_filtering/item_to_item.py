import pandas as pd
import numpy as np
from collections import deque
from scipy import spatial
from tqdm import tqdm

class ItemToItem:
    def __init__(self, catalog_items):
        self.catalog = catalog_items
        self.items_ratings = pd.DataFrame()
        self.items_similarities = pd.DataFrame()

    def load_ratings(self, db):
        '''
        For each item generates a vector containing 1 if the card is chosen in the deck, 0 if not
        :param db: database containing all decks
        '''
        ratings = deque()
        labels = range(len(db))
        for item in self.catalog:
            rating = deque()
            for j, deck in enumerate(db):
                rating.append(int(item in deck))
            ratings.append(rating)
        self.items_ratings = pd.DataFrame.from_records(ratings, index=self.catalog)

    def compute_similarities(self, db):
        '''
        Compute similarities between items
        '''

        database = db[:]
        df = pd.DataFrame(np.nan, index=self.catalog, columns=self.catalog)

        for item in tqdm(self.catalog):
            list_item = self.items_ratings.loc[item].tolist()
            if sum(list_item) == 0:
                df.at[:, item] = -1.0
                df.at[item, :] = -1.0
            else:
                for j, associated_deck in enumerate(list_item):
                    deck = database[j]
                    for card in deck:
                        if np.isnan(df.at[card, item]):
                            if card != item:
                                similarity = self.compute_cosine_angle(list_item, self.items_ratings.loc[card].tolist())
                                if np.isnan(similarity):
                                    df.at[item, card] = -1.0
                                    df.at[card, item] = -1.0
                                else:
                                    df.at[item, card] = similarity
                                    df.at[card, item] = similarity
                            else:
                                df.at[item, item] = -1.0

        self.items_similarities = df

    def get_recommendation(self, card_id, nb_recommendations):
        '''
        Return the list of the first nb_recommendations
        :param card_id: id card of which we want the recommendations
        :param nb_recommendations: number of recommendations to return
        :return: dictionary {card_id: recommendation}
        '''
        similarities = self.items_similarities.loc[card_id].sort_values(ascending=False)
        recommendations = {}
        for i in range(nb_recommendations):
            if similarities.at[i] > 0:
                recommendations[similarities.columns[i]] = similarities.at[i]
        return recommendations

    def compute_cosine_angle(self, dataset_1, dataset_2):
        return 1.0 - spatial.distance.cosine(dataset_1, dataset_2)