# -*- coding: utf-8 -*-

"""
This module implements the client's public and private interface.
"""

import os
from kayak import constants
from kayak.auth import KayakAuth
import tweet
import kayak.utils as utils


class KayakClient(object):
    """
    Base class for kayak client
    """

    def __init__(self):
        # application credentials provided by Twitter
        self.consumer_key = None
        self.consumer_secret = None

        # token used to access Twitter API
        self.bearer_token = None

        # Authentication object associated with the client
        self.auth = None

        self._check_credentials()

    # using an underscore as prefix to indicate a (semi)private method
    def _check_credentials(self):
        """
        Checks if the Twitter app credentials 'Consumer Key' and
        'Consumer Secret' are available as 'environment variables' or not.

        Invokes the authentication process if the credentials are available.
        """

        try:
            self.consumer_key = os.environ[constants.KAYAK_KEY]
            self.consumer_secret = os.environ[constants.KAYAK_SECRET]
        except KeyError:
            raise Exception
        else:
            self._authenticate()

    def _authenticate(self):
        """
        Authenticates the client using the provided credentials
        """

        self.auth = KayakAuth(self.consumer_key, self.consumer_secret)

        # update the token
        self.bearer_token = self.auth.authenticate()

    def get_tweets(self, search_query, older_tweets=True):
        """
        Returns an iterator for Twitter API responses (tweet entities).

        :param (str) search_query: Search query operator to use.
        :param (bool) older_tweets:
        If True (default), it will return the iterator containing older tweets.
        If False, it will return newer tweets on each iteration.
        """

        if type(search_query) is not str:
            raise TypeError('search_query should be a string')

        return KayakClientResponseIterator(self.bearer_token, search_query, older_tweets)


class KayakClientResponseIterator(object):
    """
    Class provides response iterator for Twitter API responses.
    Can be used to fetch new or old tweets per iteration.
    """

    def __init__(self, bearer_token, search_query, older_tweets):
        self.bearer_token = bearer_token

        self.search_query = search_query
        self.older_tweets = older_tweets

        # to work with Twitter timelines (continuously populated tweets)
        # https://dev.twitter.com/rest/public/timelines
        self.since_id = None
        self.max_id = None

    def __iter__(self):
        return self

    def next(self):
        # determine the suitable variable (since_id / max_id)
        # to use as request parameter using the direction
        _id = self.max_id if self.older_tweets else self.since_id
        _param_key = constants.TWEET_MAX_ID if self.older_tweets else constants.TWEET_SINCE_ID

        # initial execution
        if _id is None:
            res = utils.make_api_search_request(self.bearer_token, self.search_query)
        else:
            # using the suitable varialbe value saved from past executions
            params = {_param_key: _id}
            res = utils.make_api_search_request(
                self.bearer_token, self.search_query, extra_params=params)

        kayak_client_res = KayakClientResponse(res)

        # update the suitable limiting (first or last) id variable
        if self.older_tweets:
            self.max_id = kayak_client_res.last_tweet_id
        else:
            self.since_id = kayak_client_res.first_tweet_id

        return iter(kayak_client_res)


class KayakClientResponse(object):
    """
    Base class to represent and manipulate client response.
    """

    def __init__(self, response):
        self.response = response
        self.statuses = None

        # ID for the first and last tweets (unfiltered) in response
        self.first_tweet_id = None
        self.last_tweet_id = None

        self._validate_response(self.response)
        self._filter_response()

    def _validate_response(self, response):
        """
        Validates if the request was successful.
        """

        if utils.is_status_ok(response):
            self.statuses = response.json()['statuses']

            try:
                self.first_tweet_id = self.statuses[0]['id']
            except IndexError:
                raise Exception('no new tweets yet')
            else:
                self.last_tweet_id = self.statuses[-1]['id']
                return

        raise Exception

    def _filter_response(self):
        """
        Checks if a tweet object matches the given criteria or not.
        """

        self.statuses = filter(lambda x: x[constants.TWEET_RETWEET_KEY] >= constants.RETWEET_THRESHOLD, self.statuses)

    def __iter__(self):
        for status in self.statuses:
            yield tweet.KayakTweet(status)
