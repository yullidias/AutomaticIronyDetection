#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 20 19:46:19 2020

@author: yulli
"""
import src.utils.constants as cns
from src.utils.files import read_excel
import os
import glob


def length_datasets(target=cns.PATH_ANALYSIS + "length_datasets.txt"):
    with open(target, 'w') as f:
        f.write('{:30} {:>10}\n'.format("name", "length"))
        f.write('----------------------------------------------\n')
        for path in glob.glob(f"{cns.PATH_DATASETS}*.xlsx"):
            f.write('{:30} {:>10}\n'.format(os.path.basename(path),
                                            len(read_excel(path))))


if __name__ == '__main__':
    length_datasets()
