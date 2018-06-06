# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH

class ModelParameters:
    MODEL_SIM_COSINE = 0
    MODEL_SIM_PROBA = 1
    MODEL_SIM_COSINE_LSA = 2
    MODEL_SIM_COSINE_ROW = 3
    MODEL_SIM_COSINE_LSA_ROW = 4

    def __init__(self,id_run,k,n,decks, random_items, mode, color, alpha, norm_sim, model_sim, lsa_manager):
        self.k = k
        self.n = n
        self.decks = decks
        self.random_items = random_items
        self.id_run = id_run
        self.mode = mode
        self.color = color
        self.norm_sim = norm_sim
        self.similarity_model = model_sim
        self.lsa_manager = lsa_manager
        self.alpha = alpha

class ModelResults:
    def __init__(self,id_run,k,mode,color, results):
        self.id_run = id_run
        self.k = k
        self.mode = mode
        self.color = color
        self.results = results

class KeyGenerator:
    @staticmethod
    def getKey(id_run,k,mode,color):
        '''
        Return a key as a string combining all the information
        :return: string
        '''
        return str(id_run) + '_' + str(k) + '_' + str(mode) + '_' + str(color)

    @staticmethod
    def getKeyFromModelResults(model):
        return KeyGenerator.getKey(model.id_run, model.k, model.mode, model.color)

    @staticmethod
    def getKeyFromModelParameters(model):
        return KeyGenerator.getKey(model.id_run, model.k, model.mode, model.color)

    @staticmethod
    def getElements(key):
        '''
        Split the key into elements
        :param key: key as a string
        :return: array with the different elements as a string [id_run,k,mode,color_code]
        '''
        return key.split('_')
