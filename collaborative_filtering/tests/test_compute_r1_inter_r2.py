# -*- coding: utf-8 -*-
import unittest
from collaborative_filtering.item_to_item import Rating, ItemToItem
import math

class TestComputeInterBinary(unittest.TestCase):
    def setUp(self):
        "Load the sample dataset."
        self.r1 = Rating(True, 1)
        self.r2 = Rating(False, 2)

    def test_same_decks(self):
        self.r1.compression = [(1, 5)]
        self.r2.compression = [(1, 5)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 5)

    def test_one_in_common_decks(self):
        self.r1.compression = [(1, 2)]
        self.r2.compression = [(2, 3)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 1)

    def test_one_in_common_decks_reverse(self):
        self.r1.compression = [(2, 3)]
        self.r2.compression = [(1, 2)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 1)

    def test_two_in_common_decks(self):
        self.r1.compression = [(1, 3)]
        self.r2.compression = [(2, 4)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 2)

    def test_two_in_common_decks_reverse(self):
        self.r1.compression = [(2, 4)]
        self.r2.compression = [(1, 3)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 2)

    def test_included(self):
        self.r1.compression = [(1, 5)]
        self.r2.compression = [(2, 4)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 3)

    def test_included_reverse(self):
        self.r1.compression = [(2, 4)]
        self.r2.compression = [(1, 5)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 3)

    def test_cross(self):
        self.r1.compression = [(4, 6)]
        self.r2.compression = [(2, 5)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 2)

    def test_cross_inverse(self):
        self.r1.compression = [(2, 5)]
        self.r2.compression = [(4, 6)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 2)

    def test_no_common(self):
        self.r1.compression = [(1, 3)]
        self.r2.compression = [(4, 5)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 0)

    def test_no_common_reverse(self):
        self.r1.compression = [(4, 5)]
        self.r2.compression = [(1, 3)]

        intersection = ItemToItem._compute_r1_inter_r2_binary(self.r1,self.r2)
        self.assertEqual(intersection, 0)