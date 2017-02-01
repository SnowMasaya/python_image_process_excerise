# -*- coding:utf-8 -*-
# !/usr/bin/python3

from scipy.cluster.vq import *
import sift


class Vopcabulary(object):
    """
    Get the Image word vocabulary
    """
    def __init__(self, name):
        """

        """
        self.name = name
        self.voc = []
        self.idf = []
        self.trainingdata = []
        self.nbr_words = 0

    def train(self, featurefiles, k=100, subsampling=10):
        """
        Train image data
        :param featurefiles:
        :param k:
        :param subsampling:
        :return:
        """
        nbr_images = len(featurefiles)
        descr = []
        descr.append(sift.read_features_from_file(featurefiles[0])[1])
        descriptors = descr[0]
        for i in arange(1, nbr_images):
            descr.append(sift.read_features_from_file(featurefiles[1])[1])
            descriptors = vstack((descriptors, descr[i]))

