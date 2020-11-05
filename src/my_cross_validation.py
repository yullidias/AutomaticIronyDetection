#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 13 20:27:54 2020

@author: yulli
"""
import numpy as np


class CrossValidation():

    def __init__(self, n_splits, n_samples):
        self.n_splits = n_splits
        self.n_samples = n_samples
        self.TRAIN = 1
        self.VAL = 2
        self.TEST = 3

    def get_n_splits(self):
        return self.n_splits

    def get_folds(self):
        fold_sizes = np.full(self.n_splits,
                             self.n_samples // self.n_splits, dtype=np.int)
        fold_sizes[:self.n_samples % self.n_splits] += 1

        folds = []
        indices = np.arange(self.n_samples)
        current = 0
        for fold_size in fold_sizes:
            start, stop = current, current + fold_size
            folds.append(indices[start:stop])
            current = stop
        return folds

    def split_train_val_test(self):
        folds = self.get_folds()
        masc_folds = [self.TRAIN for _ in range(self.n_splits)]
        masc_folds[-2] = self.VAL
        masc_folds[-1] = self.TEST

        for split in range(self.n_splits):
            train = []
            val = []
            test = []
            for index, partition in enumerate(masc_folds):
                if partition == self.TRAIN:
                    train += list(folds[index])
                elif partition == self.VAL:
                    val += list(folds[index])
                else:
                    test += list(folds[index])
            yield train, val, test
            masc_folds = [masc_folds[-1]] + masc_folds[:-1]


if __name__ == '__main__':
    cv = CrossValidation(5, 10)
    for train, val, test in cv.split_train_val_test():
        print("Train", train)
        print("Val", val)
        print("Test", test)
