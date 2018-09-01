# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# class model for pipeline
#

from topn_recommendations.models.bpr_knn import BPRKNN
from topn_recommendations.models.item_based_deshpande import ItemBasedDeshpande

class Model:

    #List of authorized models
    BPR_KNN = 0
    ITEM_DESHPANDE = 1
    MODELS = [BPR_KNN, ITEM_DESHPANDE]

    def __init__(self, dataset, model, parameters):
        self.dataset = dataset
        self.parameters = parameters
        self.model = self._instanciate_model(model)
        self.id = dataset.id + '_' + self.model.get_name()
        if 'id' in self.parameters:
            self.id += '_' + self.parameters['id']

    def _instanciate_model(self, model):
        if model == Model.BPR_KNN:
            return BPRKNN(self.dataset.catalog, self.dataset.training_dataset, self.dataset.testing_dataset)
        else: #Item Deshpande
            return ItemBasedDeshpande(self.dataset.catalog, self.dataset.training_dataset)

    def build_model(self):
        self.model.build(self.parameters)

    def get_model(self):
        return self.model

    def save(self, path):
        self.model.save_coefficients(path + '/topN_' + self.id  + '.json')