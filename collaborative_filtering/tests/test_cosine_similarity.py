# -*- coding: utf-8 -*-
import unittest
from association_rules.apriori_analyzer import APrioriAnalyzer
from collaborative_filtering.item_to_item import Rating, ItemToItem
import math
import numpy as np

class TestCosineSimilarity(unittest.TestCase):
    def setUp(self):
        "Load the sample dataset."
        self.r1 = Rating(True)
        self.r2 = Rating(False)

    def test_no_common_decks(self):
        self.r1.compression = [1, 1]
        self.r2.compression = [1, 1]
        self.r1.norm_square = math.sqrt(1)
        self.r2.norm_square = math.sqrt(1)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertEqual(0/(self.r1.norm_square*self.r2.norm_square), cosine)

    def test_simple_common_decks(self):
        self.r1.compression = [2]
        self.r2.compression = [1, 1]
        self.r1.norm_square = math.sqrt(2)
        self.r2.norm_square = math.sqrt(1)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertEqual(1/(self.r1.norm_square*self.r2.norm_square), cosine)

    def test_no_common_decks_inverse(self):
        self.r1.compression = [1,1]
        self.r2.compression = [2]
        self.r1.norm_square = math.sqrt(1)
        self.r2.norm_square = math.sqrt(0)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertTrue(np.isnan(cosine))

    def test_common_decks(self):
        self.r1.compression = [1,1,2]
        self.r2.compression = [1,1,1,1]
        self.r1.norm_square = math.sqrt(3)
        self.r2.norm_square = math.sqrt(2)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertEqual(1/(self.r1.norm_square*self.r2.norm_square), cosine)

    def test_common_decks_2(self):
        self.r1.compression = [1,3,1]
        self.r2.compression = [1,1,1,1,1]
        self.r1.norm_square = math.sqrt(3)
        self.r2.norm_square = math.sqrt(2)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertEqual(0/(self.r1.norm_square*self.r2.norm_square), cosine)

    def test_common_decks_3(self):
        self.r1.compression = [1,1,1,1,1]
        self.r2.compression = [1,3,1]
        self.r1.norm_square = math.sqrt(3)
        self.r2.norm_square = math.sqrt(3)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertEqual(1/(self.r1.norm_square*self.r2.norm_square), cosine)

    def test_common_decks_4(self):
        self.r1.compression = [1,1,1,1,1]
        self.r2.first_value = True
        self.r2.compression = [3,1,1]
        self.r1.norm_square = math.sqrt(3)
        self.r2.norm_square = math.sqrt(4)

        cosine = ItemToItem.compute_cosine_angle_binary(self.r1,self.r2)
        self.assertEqual(3/(self.r1.norm_square*self.r2.norm_square), cosine)