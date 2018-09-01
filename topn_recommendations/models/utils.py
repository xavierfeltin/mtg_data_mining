# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH

class ModelParameters:
    def __init__(self,id_run, n, decks, random_items, mode, color):
        self.n = n
        self.decks = decks
        self.random_items = random_items
        self.mode = mode
        self.color = color
        self.id_run = id_run

    def copy(self):
        return ModelParameters(self.id_run, self.n, self.decks, self.random_items, self.mode, self.color)

class ItemDeshpandeParamerers(ModelParameters):
    MODEL_SIM_COSINE = 0
    MODEL_SIM_PROBA = 1
    MODEL_SIM_COSINE_LSA = 2
    MODEL_SIM_COSINE_ROW = 3
    MODEL_SIM_COSINE_LSA_ROW = 4

    def __init__(self,id_run, n,decks, random_items, mode, color, k, alpha, norm_sim, model_sim, lsa_manager):
        ModelParameters.__init__(self, id_run, n,decks, random_items, mode, color)
        self.k = k
        self.norm_sim = norm_sim
        self.similarity_model = model_sim
        self.lsa_manager = lsa_manager
        self.alpha = alpha

    def copy(self):
        return ItemDeshpandeParamerers(self.id_run, self.n, self.decks, self.random_items, self.mode, self.color, self.k, self.alpha,
                                       self.norm_sim, self.similarity_model, self.lsa_manager)

class BPRKNNParameters(ModelParameters):
    def __init__(self, id_run, n, decks, random_items, mode, color, lbd_I=0.05, lbd_J=0.01, learning_rate=0.01, epoch=30,
                 batch_size=50, decay=0.5, nb_early_learning = 10, min_leaning_rate = 0.025, normalize=False):
        ModelParameters.__init__(self, id_run, n,decks, random_items, mode, color)
        self.lbd_I = lbd_I
        self.lbd_J = lbd_J
        self.learning_rate = learning_rate
        self.epoch = epoch
        self.batch_size = batch_size
        self.decay = decay
        self.nb_early_learning = nb_early_learning
        self.min_leaning_rate = min_leaning_rate
        self.normalize = normalize

    def copy(self):
        return BPRKNNParameters(self.id_run, self.n, self.decks, self.random_items, self.mode, self.color, self.lbd_I,
           self.lbd_J, self.learning_rate, self.epoch, self.batch_size, self.decay, self.nb_early_learning, self.min_leaning_rate, self.normalize)

class ModelResults:
    #def __init__(self,id_run, k,mode,color, results):
    def __init__(self,id_run, mode,color, results):
        self.id_run = id_run
        #self.k = k
        self.mode = mode
        self.color = color
        self.results = results

class KeyGenerator:
    @staticmethod
    #def getKey(id_run,k,mode,color):
    def getKey(id_run,mode,color):
        '''
        Return a key as a string combining all the information
        :return: string
        '''
        #return str(id_run) + '_' + str(k) + '_' + str(mode) + '_' + str(color)
        return str(id_run) + '_'  + str(mode) + '_' + str(color)

    @staticmethod
    def getKeyFromModelResults(model):
        #return KeyGenerator.getKey(model.id_run, model.k, model.mode, model.color)
        return KeyGenerator.getKey(model.id_run, model.mode, model.color)

    @staticmethod
    def getKeyFromModelParameters(model):
        #return KeyGenerator.getKey(model.id_run, model.k, model.mode, model.color)
        return KeyGenerator.getKey(model.id_run, model.mode, model.color)

    @staticmethod
    def getElements(key):
        '''
        Split the key into elements
        :param key: key as a string
        :return: array with the different elements as a string [id_run,k,mode,color_code]
        '''
        return key.split('_')
