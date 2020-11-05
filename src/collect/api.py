import src.utils.constants as cns
from src.utils.files import read_json

import random
import tweepy


class Api(object):
    """docstring for TwitterApi."""

    def __init__(self):
        super(Api, self).__init__()
        self._tokens = read_json(cns.PATH_TOKENS)

    def __next_token(self):
        return self._tokens[random.randint(0, len(self._tokens) - 1)]

    def __twitter_api(self):
        token = self.__next_token()
        auth = tweepy.AppAuthHandler(token['api_key'], token['api_secret_key'])
        twitter_api = tweepy.API(auth, wait_on_rate_limit=True,
                         wait_on_rate_limit_notify=True, retry_count=3,
                         retry_delay=5, retry_errors=set([401, 404, 500, 503]))
        return twitter_api
