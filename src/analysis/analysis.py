#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 19 21:12:03 2020

@author: yulli
"""
import src.utils.constants as cns
from src.analysis.result_test_svm import svm_results
from src.analysis.predict import predict_all
from src.analysis.dataset import length_datasets
from src.analysis.plots import plot_all
from src.generate_data import generate_filter_data


def svm():
    print("Generate sheet for test results ... ")
    svm_results()
    generate_filter_data()
    predict_all(cns.ROOT_SVM + 'Ironics/')
    print("Generate sheet for predict results ... ")
    svm_results(root_dir=cns.PATH_PREDICT_DIR[:-1], n_folds=cns.N_SPLITS,
                name_out="predict.xlsx", has_test_dir=False)


def dataset():
    print("Generate length datasets report ...")
    length_datasets()
    print("Generate plots ...")
    plot_all()

