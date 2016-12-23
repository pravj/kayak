# -*- coding: utf-8 -*-

"""
This module facilitates custom representation of tweet entities.
"""

from kayak import constants


class KayakTweet(object):
    """
    Class to change the representation of a Tweet object.
    Currently you can access the 'text', 'id', and 'retweet count' attributes.
    """

    def __init__(self, status):
        self.status = status

        self.text = None
        self.id = None
        self.retweets = None

        self._update_values()

    def _update_values(self):
        """
        Update the custom attributes (text, id, retweets) of a tweet entity.
        """

        self.text = self.status[constants.TWEET_TEXT_KEY]
        self.id = self.status[constants.TWEET_ID_KEY]
        self.retweets = self.status[constants.TWEET_RETWEET_KEY]

    def __repr__(self):
        """
        Utilizes string representation data method (__repr__)
        so that a 'KayakTweet' object instance can be used as a string.

        :return (str): The tweet text.
        """

        return self.text
