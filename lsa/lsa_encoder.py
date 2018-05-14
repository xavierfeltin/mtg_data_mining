# -*- coding: utf-8 -*-
#
# MIT License
# Copyright (c) 2018 Xavier FOLCH
#
# Bibliography
# - http: // www.datascienceassn.org / sites / default / files / users / user1 / lsa_presentation_final.pdf
# - https: // machinelearningmastery.com / clean - text - machine - learning - python /

from random import randint
from math import ceil
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer
import unidecode
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import Normalizer
from collections import deque
import numpy as np


class DataCleaner:
    """
    Clean and prepare the data that will be used by the autoencoder
    """

    def __init__(self, data):
        self.dirty_data = data
        self.clean_data = []
        self.test_data = []
        self.training_data = []
        self.validation_data = []

    def clean(self):
        """
        Clean and homogeneize the data
        """

        max_length = len(max(self.dirty_data, key=len))
        for data in self.dirty_data:
            data = data.lower()
            data = data.replace('\n', '')
            data = unidecode.unidecode(data)
            self.clean_data.append(data.lower())# + ' ' * (max_length - len(data)))

    def prepare_data(self, ratio):
        """
        Split the data into test_data, training_data and validation_data function of the ratio set in argument
        ratio[0] corresponds to the ratio of (training_data + validation_data) versus test_data
        ratio[1] corresponds to the ratio of training_data versus validation_data
        """

        temp = self.clean_data[:]
        temp_training_data = []

        nb_data = len(self.clean_data)
        nb_training_data = ceil(nb_data * ratio[0])
        nb_test_data = nb_data -  nb_training_data

        for i in range(nb_training_data):
            index = randint(0,len(temp)-1)
            temp_training_data.append(temp[index])
            del temp[index]

        self.test_data = temp[:]

        nb_validation_data = ceil(nb_training_data * ratio[1])
        for i in range(nb_validation_data):
            index = randint(0, len(temp_training_data) - 1)
            self.validation_data.append(temp_training_data[index])
            del temp_training_data[index]

        self.training_data = temp_training_data[:]

class LSAEncoder:
    """
    Transform textual data into a vector of descriptors based on LSA algorithm
    """

    def __init__(self, documents, n_dimensions=50):
        self.text = documents
        self.n_clusters = n_dimensions
        self.vocabulary = []
        self.descriptors = []
        self.tfi = None #TFI transformation of the data with len(self.vocabulary) dimensions
        self.lsa = None #TFI transformation with reduced dimensions (self.n_dimensions) using LSA algorithm

    def tokenize(self,text):
        """
        Custom tokenizer
        Function of transformation to change the text into a vector of words based on a regular expression
        """
        tokenizer = RegexpTokenizer(r'{\w+}|\+\w+\/\+\w+|\w+\-\w+|\w+')
        tokens = tokenizer.tokenize(text)
        #tokens = [tokenizer.tokenize(content) for content in self.documents]
        tokens = [w.lower() for w in tokens]

        punctuations = ['!', '"', '#', '$', '%', '&', "'", '*', ',', '-', '.', ':', ';', '<', '=', '>', '?', '@',
                        '[', '\\', ']', '^', '_', '`', '(', '|', ')', '~']
        words = [word for word in tokens if word not in punctuations]
        stop_words = set(stopwords.words('english'))
        words = [w for w in words if not w in stop_words]

        porter = PorterStemmer()
        stemmed = [porter.stem(word) for word in words]
        return stemmed

    def tfi_transform(self):
        """
        Encode the data with the Tfid algorithm
        """
        vect = CountVectorizer(tokenizer=self.tokenize)
        dtm = vect.fit_transform(self.text)
        self.vocabulary = vect.get_feature_names()
        transformer = TfidfTransformer()
        self.tfi = transformer.fit_transform(dtm)

    def lsa_transform(self):
        """
        Reduce the number of dimensions of the tfid vector using LSA
        """
        lsa = TruncatedSVD(self.n_clusters, algorithm='arpack')
        dtm_lsa = lsa.fit_transform(self.tfi)
        self.lsa = Normalizer(copy=False).fit_transform(dtm_lsa)

    def fit(self):
        """
        Transform the original documents into vectorized data with n_cluster dimensions
        """
        #self.tokenize()
        self.tfi_transform()
        self.lsa_transform()

    def print_lsa_results(self):
        """
        Print into CSV files, the LSA reduced data
        """
        index_col = []
        for i in range(self.n_clusters):
            index_col.append('component_' + str(i))

        data_frame = pd.DataFrame(self.lsa.components_, index=index_col, columns=self.vocabulary)
        data_frame.head(10).to_csv('./test_lsa.csv')

        data_frame = pd.DataFrame(self.lsa, index=self.documents, columns=index_col)
        data_frame.head(10).to_csv('./test_lsa_reverse.csv')

    def print_similarity(self):
        """
        Print into CSV files, the similarity matrix for particular cards
        """

        similarity = np.asarray(np.asmatrix(self.lsa) * np.asmatrix(self.lsa).T)
        data_frame = pd.DataFrame(similarity, index=self.text, columns=self.text)
        data_frame.head(10).to_csv('./test_lsa_similarity.csv')

        for i in range(10):
            # sorted = data_frame.loc[i+500].sort_values(by=data_frame.iloc[i+500].name, axis=1, ascending=False)
            sorted = data_frame.iloc[i * 500].sort_values(ascending=False)
            sorted.to_csv('./similarity_card' + str(i * 500) + '.csv')

class LSAManager:
    def __init__(self, cards_content):
        self.cards_content = cards_content
        self.cards_encoded = {}
        self.encoder = None

    def encode(self):
        sorted_ids = sorted(self.cards_content.keys())
        descriptions = deque()
        for id in sorted_ids:
            descriptions.append(self.cards_content[id])


        cleaner = DataCleaner(descriptions)
        cleaner.clean()
        self.encoder = LSAEncoder(cleaner.clean_data)
        self.encoder.fit()

        encoded_content = self.encoder.lsa
        for index, vector in enumerate(encoded_content):
            self.cards_encoded[sorted_ids[index]] = vector

    def load_cards_encoding(self, encoding):
        '''
        Load the encoding of the cards from an external soource
        :param encoding: dictionary {card: encoding_array}
        '''
        for card, encoding in encoding.items():
            self.cards_encoded[card] = encoding[:]

    def get_similarity(self, card_1, list_cards):
        similarity = np.asarray(np.asmatrix(self.cards_encoded[card_1]) * np.asmatrix(self.cards_encoded[list_cards]).T)
        return similarity[0,0]