#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 21 11:01:09 2020

@author: yulli
"""

import src.utils.constants as cns
from src.utils.files import read_excel
from src.utils.files import remove_extension
from src.utils.files import create_if_not_exists
from src.generate_vocabulary import get_features
from src.generate_vocabulary import get_feature_names
from src.preprocess import remove_irrelevant_punctuation

import glob
import os
import matplotlib.pyplot as plt
from yellowbrick.text import FreqDistVisualizer
from yellowbrick.text import DispersionPlot
from yellowbrick.classifier import ConfusionMatrix


def plot_confusion_matrix(clf_fitted, X_test, y_test, out_path):
    cm = ConfusionMatrix(clf_fitted, classes=list(set(y_test)))
    cm.score(X_test, y_test)
    cm.show(outpath=out_path + 'confusion_matrix.png')
    plt.gcf().clear()  # forget plot


def plot_most_freq_words(out_path, X, feature_names):
    visualizer = FreqDistVisualizer(features=feature_names, n=20)
    visualizer.fit(X)

    # Call finalize to draw the final yellowbrick-specific elements
    visualizer.finalize()

    # plt.show()
    # plt.savefig(out_path + '-frequency.png', dpi=300)

    visualizer.show(outpath=out_path + '-frequency.png', clear_figure=True,
                    dpi=300)
    plt.gcf().clear()  # forget plot


def plot_dispersion(out_path, df):
    # Create a list of words from the corpus text
    text = [remove_irrelevant_punctuation(doc) for doc in df['text']]

    # Choose words whose occurence in the text will be plotted
    target_words = ['marcacao', 'numero', 'https', 'muito', 'ja',
                    'reticencias', 'hashtag']

    # Create the visualizer and draw the plot,
    visualizer = DispersionPlot(target_words)
    visualizer.fit(text)
    visualizer.show(outpath=out_path + '-dispersion.png')


def plots(path_dataset, bow_ngram, target_name):
    dataset = read_excel(path_dataset, suffle=True)
    features = get_features(dataset['text'], bow_ngram)
    feature_names = get_feature_names(bow_ngram)

def get_name(path, bow_ngram):
    dataset_name = remove_extension(os.path.basename(path), '.xlsx')
    sbn = 'bow_ngram' if bow_ngram else 'bow'
    return dataset_name + '-' + sbn


def plot_all(out_dir=cns.PATH_PLOT):
    create_if_not_exists(out_dir)
    for bow_ngram in [True, False]:
        for path in glob.glob(cns.PATH_TRAIN_DIR + '*.xlsx'):
            dataset = read_excel(path)
            features = get_features(dataset['text'], bow_ngram)
            feature_names = get_feature_names(bow_ngram)
            target_name = out_dir + get_name(path, bow_ngram)
            if path != cns.D_NOT_IRONIC:
                print(os.path.basename(path))
                print("Plot frequency ...")
                plot_most_freq_words(target_name, features, feature_names)
                plot_most_freq_words(target_name + "-ironics",
                                     get_features(dataset[dataset['label'] == 1]['text'], bow_ngram),
                                     feature_names)
                plot_most_freq_words(target_name + "-notironics",
                                     get_features(dataset[dataset['label'] == 0]['text'], bow_ngram),
                                     feature_names)


if __name__ == '__main__':
    dataset = read_excel(cns.PATH_TEMP_DIR + "poquer.xlsx", suffle=True)
    bow_ngram = True
    features = get_features(dataset['text'], bow_ngram)
    feature_names = get_feature_names(bow_ngram)

    plots(cns.PATH_TEMP_DIR + "poquer.xlsx", bow_ngram,
          cns.PATH_TEMP_DIR + 'test')

    plot_most_freq_words(cns.PATH_TEMP_DIR + "teste", features, feature_names)
