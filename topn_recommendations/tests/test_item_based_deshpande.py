# -*- coding: utf-8 -*-

import unittest
import numpy as np
import pandas as pd
from collaborative_filtering.item_to_item import ItemToItem
from topn_recommendations.models.item_based_deshpande import ItemBasedDeshpande

class TestItemBasedDeshpande(unittest.TestCase):

    def setUp(self):
        self.catalog_items = ['a','b','c']
        self.built_deck = [1]
        self.recommander = ItemToItem(self.catalog_items)
        self.recommander.items_similarities = pd.DataFrame(0, index=self.recommander.catalog, columns=self.recommander.catalog)
        for i in range(3):
            for j in range(3):
                self.recommander.items_similarities.at[self.catalog_items[i],self.catalog_items[j]] = i+j

    def testBuildModel(self):
        modelTopN = ItemBasedDeshpande(self.catalog_items,[])
        modelTopN.build_model(2, ItemToItem.compute_cosine_angle_binary,recommender=self.recommander)

        self.assertEqual(len(modelTopN.model), 3)
        self.assertListEqual(modelTopN.model['a'].values.tolist(), [0,1,2])
        self.assertListEqual(modelTopN.model['b'].values.tolist(), [0,2,3])
        self.assertListEqual(modelTopN.model['c'].values.tolist(), [0,3,4])

    def testGetTopNRecommendations(self):
        modelTopN = ItemBasedDeshpande(self.catalog_items, [])
        modelTopN.build_model(2, ItemToItem.compute_cosine_angle_binary, recommender=self.recommander)
        recommendations = modelTopN.get_top_N_recommendations(self.built_deck, 2)

        self.assertEqual(len(recommendations), 1)
        self.assertEqual(recommendations['c'], 3)