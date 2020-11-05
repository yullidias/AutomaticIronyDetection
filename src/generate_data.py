#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 28 21:29:32 2020

@author: yulli
"""
# -*- coding: utf-8 -*-
import src.utils.constants as cns
from src.utils.files import read_excel, to_excel

import os
import pandas as pd
import shutil


def get_balanced(df):
    class_by_label = df.loc[:, ['id', 'label']].groupby('label').count()
    nclasses = min(class_by_label.loc[cns.IRONIC_LABEL, 'id'],
                   class_by_label.loc[cns.NOT_IRONIC_LABEL, 'id'])
    ironic_df = df[df['label'] == cns.IRONIC_LABEL]
    ironic_df = ironic_df.sample(n=nclasses, random_state=cns.SEED)

    not_ironic_df = df[df['label'] == cns.NOT_IRONIC_LABEL]
    not_ironic_df = not_ironic_df.sample(n=nclasses, random_state=cns.SEED)

    return pd.concat([ironic_df, not_ironic_df])


def save_data(out_name, paths, out_dir, balanced=cns.BALANCED_DATASET):
    df = read_excel(paths, suffle=False)

    if balanced:
        df = get_balanced(df)

    to_excel(f"{out_dir}{out_name}.xlsx",
             df.sample(frac=1, random_state=cns.SEED))


def generate_train_data(out_dir=cns.PATH_TRAIN_DIR):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    print("Generate train directory ...")
    save_data("Ironics", [cns.D_IRONIC, cns.D_NOT_IRONIC], out_dir)

def generate_filter_data(out_dir=cns.PATH_FILTER_DIR):
    if os.path.exists(out_dir):
        shutil.rmtree(out_dir)

    save_data("Conjunto-ironia", [cns.D_IRONIA, cns.D_NOT_IRONIC], out_dir,
              balanced=False)
    save_data("Conjunto-soquenao", [cns.D_SOQUENAO, cns.D_NOT_IRONIC], out_dir,
              balanced=False)
    save_data("Conjunto-sqn", [cns.D_SQN, cns.D_NOT_IRONIC], out_dir, balanced=False)
    save_data("Conjunto-hashtags", [cns.D_HASHTAG, cns.D_NOT_IRONIC], out_dir,
              balanced=False)
    save_data("Conjunto-manual", [cns.D_M_IRONIC, cns.D_NOT_IRONIC], out_dir,
              balanced=False)
