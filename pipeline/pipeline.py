# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Pipeline manages the different steps of building models
#

import sys
from multiprocessing import Pool, Manager
from pipeline.dataset import Dataset
from pipeline.model import Model
from collections import deque

class Pipeline:

    FAIL = -1
    SUCCESS = 0

    def __init__(self):
        self.datasets = []
        self.models = {}
        self.results = {Pipeline.SUCCESS: [], Pipeline.FAIL: []}

    def add_dataset(self, id, serie, catalog=None):
        new_dataset = Dataset(id, catalog)
        new_dataset.append_serie(serie)
        self.datasets.append(new_dataset)

    def add_model(self, model, parameters):
        '''
        Add a model and its regression parameters to the pipeline
        :param model: model constant defned in the Pipeline class
        :param parameters: hash containing the parameters for the model
        '''
        if model not in Model.MODELS:
            raise TypeError(model + ' is not a valid model')

        if model not in self.models:
            self.models[model] = []

        self.models[model].append(parameters)

    def prepare(self):
        '''
        Prepare the data by splitting the datasets into training and testing sets
        :return: none
        '''
        for dataset in self.datasets:
            dataset.prepare()

    def build(self):
        '''
        Generate the models based on the datasets
        :return: none
        '''
        model_instances = deque()
        for dataset in self.datasets:
            for model, list_parameters in self.models.items():
                for parameters in list_parameters:
                    model_instances.append(Model(dataset, model, parameters))

        results_queue = self._process_models(model_instances)

        while not results_queue.empty():
            result = results_queue.get()
            if result[1] != '':
                self.results[Pipeline.FAIL].append(result[0])
                print('Model ' + result[0].id + ' has failed when building because ' + result[1], file=sys.stderr)
            else:
                self.results[Pipeline.SUCCESS].append(result[0])

    def save(self, path):
        '''
        Save successful built models into json files with the name path/id.json
        Save associated datasets catalogs
        '''

        for model in self.results[Pipeline.SUCCESS]:
            model.save(path)

    def _process_models(self, model_instances):
        '''
        Producer / Consumer model for multithreading
        :return: queue with the models built
        '''

        number_wokers = 6
        manager = Manager()
        pool = Pool(processes=number_wokers)
        jobs_queue = manager.Queue()
        results_queue = manager.Queue()

        for model in model_instances:
            jobs_queue.put(model)

        # stop workers
        for i in range(number_wokers):
            jobs_queue.put(None)

        for i in range(number_wokers):
            _ = pool.apply_async(Pipeline._worker, (i, jobs_queue, results_queue))

        pool.close()
        pool.join()
        return results_queue

    @staticmethod
    def _worker(id, jobs_queue, results_queue):
        while True:
            model = jobs_queue.get()
            if model is None:
                return 0

            try:
                model.build_model()
                results_queue.put((model, ''))
            except Exception as err:
                results_queue.put((model, str(err)))
