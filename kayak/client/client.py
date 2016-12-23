# -*- coding: utf-8 -*-

"""
kayak.client

This module implements the client interface
"""

import os
import urllib
import requests as r
from kayak import constants
from kayak.auth import KayakAuth
from tweet import KayakTweet


def _make_request(bearer_token, extra_params=None):
    headers = {}
    headers['Authorization'] = '{0} {1}'.format(constants.BEARER_AUTH_HEADER_PREFIX, bearer_token)

    # maximum number of tweets returned by Twitter API per page
    n = 100

    # %escape the hashtag value to prevent duplication as a URI fragment
    params = {'count': n, 'q': urllib.quote(constants.HASHTAG)}

    # append additional request parameters
    if extra_params is not None:
        for k in extra_params:
            params[k] = extra_params[k]

    try:
        res = r.get(constants.SEARCH_API_URL, headers=headers, params=params)
    except Exception, e:
        raise e
    else:
        return res


class KayakClient(object):
    """
    kayak.client.KayakClient
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

        :raises: Error if they are unavailable
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

    def get_tweets(self, older_tweets=True):
        """
        Returns an iterator for Twitter API responses.
        """

        return KayakClientResponseIterator(self.bearer_token, older_tweets)


class KayakClientResponse(object):
    """
    kayak.client.KayakClientResponse
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

        if (response.status_code == r.codes.ok):
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

        # TODO: use 'filter'(built-in) based implementation 

        _filtered_tweets = []

        for status in self.statuses:
            if (status[constants.TWEET_RETWEET_KEY] >= constants.RETWEET_THRESHOLD):
                _filtered_tweets.append(status)

        self.statuses = _filtered_tweets

    def __iter__(self):
        for status in self.statuses:
            yield KayakTweet(status)


class KayakClientResponseIterator(object):
    """
    Returns iterator for Twitter API responses.
    Used to fetch new or old tweets per iteration.
    """

    def __init__(self, bearer_token, older_tweets):
        self.older_tweets = older_tweets
        self.bearer_token = bearer_token

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
            res = _make_request(self.bearer_token)
        else:
            # using the suitable varialbe value saved from past executions
            params = {_param_key: _id}
            res = _make_request(self.bearer_token, extra_params=params)

        kayak_client_res = KayakClientResponse(res)

        # update the suitable limiting (first or last) id variable
        if self.older_tweets:
            self.max_id = kayak_client_res.last_tweet_id
        else:
            self.since_id = kayak_client_res.first_tweet_id

        return iter(kayak_client_res)
