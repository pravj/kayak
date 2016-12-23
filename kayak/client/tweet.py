# -*- coding: utf-8 -*-

"""
This module implements custom representation of tweet entities.
"""

from kayak import constants


class KayakTweet(object):
    """
    kayak.client.KayakTweet

    Custom representation of a Tweet object.
    """

    def __init__(self, status):
        self.status = status

        self.text = None
        self.id = None
        self.retweets = None

        self._update_values()

    def _update_values(self):
        self.text = self.status[constants.TWEET_TEXT_KEY]
        self.id = self.status[constants.TWEET_ID_KEY]
        self.retweets = self.status[constants.TWEET_RETWEET_KEY]

    def __repr__(self):
        """
        Utilizes string representation data method (__repr__)
        so that a 'KayakTweet' object instance can be used as a string.
        """

        return self.text
