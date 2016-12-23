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

        # used to work with Twitter timelines (continuously populated tweets)
        # https://dev.twitter.com/rest/public/timelines
        self.since_id = None

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

    def _make_request(self, extra_params=None):
        headers = {}
        headers['Authorization'] = '{0} {1}'.format(constants.BEARER_AUTH_HEADER_PREFIX, self.bearer_token)

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

    def get_tweets(self):
        """
        Collect newer tweets since last execution
        """

        # initial execution of the client
        if self.since_id is None:
            res = self._make_request()
        else:
            params = {'since_id': self.since_id}
            res = self._make_request(extra_params=params)

        kayak_client_res = KayakClientResponse(res)

        # update 'since_id' for future use
        self.since_id = kayak_client_res.first_tweet_id

        return iter(kayak_client_res)


class KayakClientResponse(object):
    """
    kayak.client.KayakClientResponse
    """

    def __init__(self, response):
        self.response = response
        self.statuses = None

        # ID for the first tweet (unfiltered) in response
        self.first_tweet_id = None

        self._validate_response(self.response)
        self._filter_tweets()

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
                return

        raise Exception

    def _filter_tweets(self):
        """
        Checks if a tweet object matches the given criteria or not.
        """

        # Because a one-liner wasn't looking good

        _filtered_tweets = []

        for status in self.statuses:
            if (status[constants.TWEET_RETWEET_KEY] >= constants.RETWEET_THRESHOLD):
                _filtered_tweets.append(status)

        self.statuses = _filtered_tweets

    def __iter__(self):
        for status in self.statuses:
            yield KayakTweet(status)


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
