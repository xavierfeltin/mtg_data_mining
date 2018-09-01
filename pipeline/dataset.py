# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Dataset manages the data fed to the pipeline
#

import json
from collections import deque
from random import randint

class Dataset:
    def __init__(self, id, catalog = None):
        self.id = id

        if catalog is None:
            self.catalog = deque()
        else:
            self.catalog = catalog[:]

        self.dataset = deque()
        self.training_dataset = deque()
        self.testing_dataset = deque()

    def append(self, data):
        self.dataset.append(data[:])

    def append_serie(self, serie):
        for data in serie:
            self.append(data)

    def prepare(self):
        '''
        Prepare the data by splitting the datasets into training and testing sets
        :return: none
        '''

        for data in self.dataset:
            index = randint(0, len(data) - 1)
            self.testing_dataset.append(data[index])
            self.training_dataset.append(data[:])

        for j, item in enumerate(self.testing_dataset):
            self.training_dataset[j].remove(item)

    def save_catalog(self, path):
        with open(path + '/catalog_' + self.id + '.json', 'w') as f:
            json_data = []
            for elt in self.catalog:
                json_data.append(elt.to_json())
            json.dump(json_data, f)
