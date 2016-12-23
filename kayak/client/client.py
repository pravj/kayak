# -*- coding: utf-8 -*-

"""
kayak.client

This module implements the client interface
"""

import os
from kayak import constants


class KayakClient(object):
    """
    kayak.client.KayakClient
    """

    def __init__(self):
        # application credentials provided by Twitter
        self.consumer_key = None
        self.consumer_secret = None

        self._check_credentials()

    # using an underscore as prefix to indicate a (semi)private method
    def _check_credentials(self):
        """
        Checks if the Twitter app credentials 'Consumer Key' and
        'Consumer Secret' are available as 'environment variables' or not.

        :raises: Error if they are unavailable
        """

        try:
            self.consumer_key = os.environ[constants.KAYAK_KEY]
            self.consumer_secret = os.environ[constants.KAYAK_SECRET]
        except KeyError:
            raise Exception
