# -*- coding: utf-8 -*-

# Name of the environment variable used to store the 'Consumer Key'
KAYAK_KEY = 'KAYAK_CONSUMER_KEY'

# environment variable to store the 'Consumer Secret'
KAYAK_SECRET = 'KAYAK_CONSUMER_SECRET'

# header prefix used in different types of authentications
AUTH_HEADER_PREFIX = 'Basic'
BEARER_AUTH_HEADER_PREFIX = 'Bearer'

# request attributes
REQ_USER_AGENT = 'Kayak@hackpravj-v1.0.0'
REQ_ENCODING = 'gzip'
REQ_CONTENT_TYPE = 'application/x-www-form-urlencoded;charset=UTF-8'
REQ_DATA = {'grant_type': 'client_credentials'}

# URLs to 'request' a new token or 'invalidate' an existing token
REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth2/token'
INVALIDATE_TOKEN_URL = 'https://api.twitter.com/oauth2/invalidate_token'

# key-value pair to match in order to verify correctness of response
VERIFICATION_KEY = 'token_type'
VERIFICATION_VALUE = 'bearer'

# key name associated with the token
TOKEN_KEY = 'access_token'

# hashtag to look for
HASHTAG = '#custserv'

# URL for Twitter search API
SEARCH_API_URL = 'https://api.twitter.com/1.1/search/tweets.json'


__all__ = [
			KAYAK_KEY,
			KAYAK_SECRET,
			AUTH_HEADER_PREFIX,
			BEARER_AUTH_HEADER_PREFIX,
			REQ_USER_AGENT,
			REQ_ENCODING,
			REQ_CONTENT_TYPE,
			REQ_DATA,
			REQUEST_TOKEN_URL,
			INVALIDATE_TOKEN_URL,
			VERIFICATION_KEY,
			VERIFICATION_VALUE,
			TOKEN_KEY,
			HASHTAG,
			SEARCH_API_URL]