#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 10 15:51:17 2020

@author: yulli
"""

import src.utils.constants as cns
from src.utils.files import to_excel
from src.utils.effects import progress_bar
from src.collect.user import User

import pandas as pd
import glob


def generate(target_file):
    print("Generate user dataset ...")
    user_df = pd.DataFrame(columns=['id', 'created_at', 'verified',
                                    'number_of_tweets', 'friends',
                                    'followers', 'favourites',
                                    'location', 'has_profile_image',
                                    'has_background_image'])
    list_users = glob.glob(cns.ROOT_COLLECT_USERS + '*.json')
    for count, path in enumerate(list_users):
        user = User(path)
        columns = {
             "id": user.id(),
             "created_at": user.created_at(),
             "verified": user.is_verified(),
             "number_of_tweets": user.number_of_tweets(),
             "friends": user.friends_count(),
             "followers": user.followers_count(),
             "favourites": user.favourites_count(),
             "location": user.location(),
             "has_profile_image": user.has_own_profile_image(),
             "has_background_image": user.has_own_theme_or_background()
             }
        user_df = user_df.append(columns, ignore_index=True)
        progress_bar(count + 1, len(list_users))

    if not target_file.endswith('.xslx'):
        target_file += '.xlsx'

    to_excel(target_file, user_df)


if __name__ == '__main__':
    print("Generate users dataset ...")
    generate(cns.ROOT_DATA + 'users')
    print("DONE!")
