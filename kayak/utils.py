# -*- coding: utf-8 -*-

"""
This module implements utility functions for the client.
"""

import urllib
import requests as r
from kayak import constants


def make_api_search_request(bearer_token, extra_params=None):
    """
    Makes a GET request to Twitter Search API endpoint
    with given request parameters.

    :return: Response object for the GET request.
    """

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

def make_api_post_request(url, headers, payload):
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

def is_status_ok(res):
    """
    Returns True if status code is equal to 200.

    :return (bool): If status code was 200 or not.
    """

    return res.status_code == r.codes.ok


__all__ = ['make_api_search_request', 'make_api_post_request', 'is_status_ok']