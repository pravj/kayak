# -*- coding: utf-8 -*-

"""
This module implements utility functions for the client.
"""


import types
import urllib
import requests as r
from kayak import constants


def make_api_search_request(bearer_token, search_query, extra_params=None):
    """
    Makes a GET request to Twitter Search API endpoint
    with given request parameters.

    :param (str) bearer_token: Bearer token to use in authorization headers.
    :param (str) search_query: Search API query string.

    :return: Response object for the GET request.
    """

    headers = {}
    headers['Authorization'] = '{0} {1}'.format(constants.BEARER_AUTH_HEADER_PREFIX, bearer_token)

    # maximum number of tweets returned by Twitter API per page
    n = 100

    # %escape the query value
    params = {'count': n, 'q': urllib.quote(search_query)}

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

def is_str(obj):
    """
    Check is an object is string.

    :return (bool): True if the object is string.
    """

    return isinstance(obj, str)

def is_int(obj):
    """
    Check is an object is integer.

    :return (bool): True if the object is integer.
    """

    return isinstance(obj, int)

def is_func(obj):
    """
    Check is an object is function.

    :return (bool): True if the object is function.
    """

    return isinstance(obj, types.FunctionType)


__all__ = [
            'make_api_search_request',
            'make_api_post_request',
            'is_status_ok',
            'is_str',
            'is_int',
            'is_func']
