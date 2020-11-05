#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr  6 18:16:36 2020

@author: yulli
"""
import src.utils.constants as cns
from src.collect.tweet import Tweet
from src.utils.files import write_list
from src.utils.files import read_sample
from src.utils.effects import progress_bar
import random
import glob
import argparse


def generate(source_dir, target_file, n_items, list_to_ignore):
    random.seed(cns.SEED)
    tweets = glob.glob(source_dir + '*.json')
    sample = []
    progress_bar(0, n_items)
    count_items = 0
    while count_items < n_items and len(tweets) != 0:
        choosed = tweets[random.randint(0, len(tweets)-1)]
        tweet = Tweet(choosed)
        if not tweet.is_retweet() and tweet.id() not in list_to_ignore:
            sample.append(tweet.id())
            count_items += 1
            progress_bar(count_items, n_items)

        tweets.remove(choosed)
    write_list(target_file, sample)
    if len(sample) != n_items:
        print(f"Couldn't generate a sample with {n_items} items. "
              f"A sample with {len(sample)} was generated.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Create datasets.")
    parser.add_argument('-v', '--valid_sample', action='store_true',
                        help="Generate real datasets")
    args = parser.parse_args()

    if args.valid_sample:
        print("Generate preprocess sample ...")
        ignore_tweets = read_sample(cns.UNLABLED_SAMPLE)
        generate(cns.PATH_STOPWORDS, cns.PREPROCESS_SAMPLE, 10**5,
                 ignore_tweets)
    else:
        s_dir = cns.ROOT_DATA + 'temp/jsons/'
        generate(s_dir, cns.ROOT_DATA + 'temp/sample-test.txt', 10,
                 ['1129184408106201088', '1127340537021964288'])
