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

    def _make_request(self, n):
        headers = {}
        headers['Authorization'] = '{0} {1}'.format(constants.BEARER_AUTH_HEADER_PREFIX, self.bearer_token)

        params = {'count': n, 'q': urllib.quote(constants.HASHTAG)}

        try:
            res = r.get(constants.SEARCH_API_URL, headers=headers, params=params)
        except Exception, e:
            raise e
        else:
            return res

    def get_tweets(self, n=15):
        res = self._make_request(n)
        return res