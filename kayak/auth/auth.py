# -*- coding: utf-8 -*-

"""
This module manages the authentication process for the client.
"""

import requests as r
from base64 import b64encode
from kayak import constants


class KayakAuth(object):
    """
    Base authentication class for the KayakClient.

    It uses the 'application-only authentication flow' of Twitter API.
    https://dev.twitter.com/oauth/application-only
    """

    def __init__(self, key, secret):
        self.key = key
        self.secret = secret

    def authenticate(self):
        """
        Returns the 'Bearer' token after a successful authentication.

        :return (str): Bearer token to use in authorization header.
        """

        headers = self._prepare_headers()
        payload = constants.REQ_DATA

        response = self._make_request(
            constants.REQUEST_TOKEN_URL, headers, payload)

        if (self._verify_response(response)):
            return response.json()[constants.TOKEN_KEY]

    def invalidate_token(self, bearer_token):
        """
        Returns True if the 'Bearer' token is successfully invalidated.

        :return (bool): If the token was invalidated or not.
        """

        headers = self._prepare_headers()
        payload = {constants.TOKEN_KEY: bearer_token}

        try:
            response = self._make_request(
                constants.INVALIDATE_TOKEN_URL, headers, payload)
        except Exception, e:
            return False
        else:
            return True

    def _prepare_headers(self):
        """
        Returns request headers needed for the
        'application-only authentication flow' instructed by Twitter

        :return (dict): Dictionary containing request headers.
        """

        encoded_key = self.key.encode('utf-8')
        encoded_secret = self.secret.encode('utf-8')

        concatenated_creds = '{0}:{1}'.format(encoded_key, encoded_secret)
        encoded_creds = b64encode(concatenated_creds.encode('utf-8'))

        headers = {'User-Agent': constants.REQ_USER_AGENT}
        headers['Accept-Encoding'] = constants.REQ_ENCODING
        headers['Content-Type'] = constants.REQ_CONTENT_TYPE
        headers['Authorization'] = '{0} {1}'.format(
            constants.AUTH_HEADER_PREFIX, encoded_creds.decode('utf-8'))

        return headers

    def _make_request(self, url, headers, payload):
        """
        Returns the response for a POST request
        made at an endpoint with given request attributes.

        :return: Response object for the POST request.
        """

        try:
            res = r.post(url, headers=headers, data=payload)
        except Exception, e:
            raise e
        else:
            return res

    def _verify_response(self, res):
        """
        Returns that the response follows the Twitter guidelines or not.

        :return (bool): If the response is valid or not.
        """

        if (res.json()[constants.VERIFICATION_KEY] == constants.VERIFICATION_VALUE):
            return True

        return False
