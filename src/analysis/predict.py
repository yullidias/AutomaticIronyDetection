#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  3 16:30:41 2020

@author: yulli
"""
import src.utils.constants as cns
from src.generate_vocabulary import get_features
from src.utils.files import write_json
from src.utils.files import read_excel
from src.utils.files import to_excel
from src.utils.files import remove_extension
from src.utils.files import read_obj
from src.analysis.plots import plot_confusion_matrix


import os
import shutil
import glob
import re
import pandas as pd
from sklearn.metrics import classification_report, confusion_matrix


def log_results(path, shape, fold, clf, score, report, confusion_matrix):
    values = {
        "fold": int(fold),
        "size": shape,
        "score": score,
        "report": report,
        "confusion_matriz": confusion_matrix.tolist(),
        "parameters": clf.get_params(),
    }
    write_json(path + "predict.json", values)
    return values


def predict(fold, df, bow_ngram, clf, out_dir):
    directory = out_dir + fold + '/'
    X = get_features(df['text'], bow_ngram)
    y = df['label']
    predicted = clf.predict(X)
    report = classification_report(y, predicted, output_dict=True)
    cm = confusion_matrix(y, predicted)
    score = report['macro avg']['f1-score']

    log_results(directory, X.shape, fold, clf, score, report, cm)
    plot_confusion_matrix(clf, X, y, directory)

    return clf.predict(X)


def get_fold(path):
    return re.findall(r'/[0-9]*/', path)[0][1]


def predict_all(svm_dir, source_dir=cns.PATH_FILTER_DIR,
                out_dir=cns.PATH_PREDICT_DIR):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)
    for dataset_name in os.listdir(source_dir):
        df = read_excel(source_dir + dataset_name)
        name = remove_extension(dataset_name, '.xlsx')
        print("Predict " + name + " ...")
        for bow_ngram in [True, False]:
            bn = 'bow_ngram' if bow_ngram else 'bow'
            for path_obj in glob.glob(svm_dir + bn + '/[0-9]*/test/*.obj'):
                clf = read_obj(path_obj)
                predict(get_fold(path_obj), df, bow_ngram, clf,
                        f"{out_dir}{name}/{bn}/")
