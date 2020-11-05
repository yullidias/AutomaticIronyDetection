#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 19:24:51 2020

@author: yulli
"""
import src.utils.constants as cns
from src.utils.files import read_json


class ResultSVM():
    def __init__(self, path):
        self._result = read_json(path)

    def c(self):
        return self._result["c"]

    def score(self):
        return self._result["score"]

    def fold(self):
        return self._result['fold']

    def accuracy(self):
        return self._result['report']['accuracy']

    def macro_f1(self):
        return self._result['report']['macro avg']['f1-score']

    def _f1_score(self, label):
        return self._result['report'][str(label)]['f1-score']

    def _precision(self, label):
        return self._result['report'][str(label)]['precision']

    def _recall(self, label):
        return self._result['report'][str(label)]['recall']

    def ironic_f1_score(self):
        return self._f1_score(cns.IRONIC_LABEL)

    def ironic_precision(self):
        return self._precision(cns.IRONIC_LABEL)

    def ironic_recall(self):
        return self._recall(cns.IRONIC_LABEL)

    def not_ironic_f1_score(self):
        return self._f1_score(cns.NOT_IRONIC_LABEL)

    def not_ironic_precision(self):
        return self._precision(cns.NOT_IRONIC_LABEL)

    def not_ironic_recall(self):
        return self._recall(cns.NOT_IRONIC_LABEL)

    def size_partition(self):
        return self._result['size_partition']
