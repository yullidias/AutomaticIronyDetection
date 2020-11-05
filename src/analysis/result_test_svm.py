#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Sun Apr 19 18:37:19 2020

@author: yulli
'''
import src.utils.constants as cns
from src.analysis.parse_result_svm import ResultSVM
from src.utils.files import to_excel
from src.utils.files import to_markdown

import numpy as np
import pandas as pd
import seaborn as sns
from scipy import stats
import os
import glob


def get_result_test(n_folds, dataset_name, bow_ngram_str, root_dir,
                    has_test_dir):
    result = pd.DataFrame(columns=np.arange(n_folds).tolist() +
                          ['avg', 'median', 'mode', 'std'],
                          index=['macro-f1',
                                 'accuracy',
                                 'score',
                                 '[ironic] f1',
                                 '[ironic] precision',
                                 '[ironic] recall',
                                 '[not ironic] f1',
                                 '[not ironic] precision',
                                 '[not ironic] recall'],
                          dtype='float')
    test = 'test/' if has_test_dir else ""
    paths = glob.glob(
            f'{root_dir}/{dataset_name}/{bow_ngram_str}/[0-9]/{test}*.json')
    for path in paths:
        rst = ResultSVM(path)
        fold = rst.fold()
        result.loc['macro-f1'][fold] = rst.macro_f1()
        result.loc['accuracy'][fold] = rst.accuracy()
        result.loc['score'][fold] = rst.score()
        result.loc['[ironic] f1'][fold] = rst.ironic_f1_score()
        result.loc['[ironic] precision'][fold] = rst.ironic_precision()
        result.loc['[ironic] recall'][fold] = rst.ironic_recall()
        result.loc['[not ironic] f1'][fold] = rst.not_ironic_f1_score()
        result.loc['[not ironic] precision'][fold] = rst.not_ironic_precision()
        result.loc['[not ironic] recall'][fold] = rst.not_ironic_recall()

    # Calculate the average
    for idx in result.index:
        result.loc[idx]['avg'] = np.nanmean(result.loc[idx])
        result.loc[idx]['median'] = np.nanmedian(result.loc[idx])
        result.loc[idx]['mode'] = stats.mode(result.loc[idx]).mode[0]
        result.loc[idx]['std'] = np.std(result.loc[idx])
    return result


def format_df(df):
    cm = sns.light_palette("green", as_cmap=True)
    return df.style.background_gradient(cmap=cm)


def resume_results(dfs, sheets_name):
    select_svg = [df.loc[:, 'avg'] for df in dfs]
    resume_df = pd.concat(select_svg, axis=1)
    resume_df.columns = sheets_name
    return resume_df, 'resume-avg'


def svm_results(root_dir=cns.ROOT_SVM, n_folds=cns.N_SPLITS,
                 name_out="result-partition-test.xlsx", has_test_dir=True):
    results = []
    sheets_names = []
    for dataset_name in os.listdir(root_dir):
        for bow_ngram_str in ['bow_ngram', 'bow']:
            result_df = get_result_test(n_folds, dataset_name, bow_ngram_str,
                                        root_dir, has_test_dir)
            results.append(result_df)
            sheets_names.append(dataset_name + '_' + bow_ngram_str)
    resume_df, sheet_name = resume_results(results, sheets_names)
    results.append(resume_df)
    sheets_names.append(sheet_name)
    to_markdown(cns.PATH_ANALYSIS_SVM + name_out, results,
                file_name=sheets_names)
    results = [format_df(df) for df in results]
    to_excel(cns.PATH_ANALYSIS_SVM + name_out, results,
             sheet_name=sheets_names)


if __name__ == "__main__":
    svm_results()
