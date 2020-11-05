from src.utils.files import read_json


class Tweet(object):
    """docstring for Tweet."""

    def __init__(self, filename):
        super(Tweet, self).__init__()
        self._tweet = read_json(filename)

    def id(self):
        return self._tweet["id_str"]

    def user_id(self):
        return self._tweet["user"]["id_str"]

    def is_retweet(self):
        return "retweeted_status" in self._tweet

    def reply_to_status(self):
        return self._tweet["in_reply_to_status_id_str"]

    def reply_to_user(self):
        return self._tweet["in_reply_to_user_id_str"]

    def retweet_count(self):
        return self._tweet["retweet_count"]

    def favorite_count(self):
        return self._tweet["favorite_count"]

    def language(self):
        return self._tweet["lang"]

    def get_text(self):
        if "full_text" in self._tweet:
            return self._tweet["full_text"]
        if "text" in self._tweet:
            return self._tweet["text"]
        return None
