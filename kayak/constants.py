# -*- coding: utf-8 -*-

# Name of the environment variable used to store the 'Consumer Key'
KAYAK_KEY = 'KAYAK_CONSUMER_KEY'

# environment variable to store the 'Consumer Secret'
KAYAK_SECRET = 'KAYAK_CONSUMER_SECRET'

# header prefix used in different types of authentications
AUTH_HEADER_PREFIX = 'Basic'
BEARER_AUTH_HEADER_PREFIX = 'Bearer'

# request attributes
REQ_USER_AGENT = 'Kayak@hackpravj-v0.0.9'
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

# minimum number of re-tweets required
RETWEET_THRESHOLD = 1

# URL for Twitter search API
SEARCH_API_URL = 'https://api.twitter.com/1.1/search/tweets.json'

# Keys to look for in 'status' response
# in case of breaking changes in Twitter API results
TWEET_TEXT_KEY = 'text'
TWEET_ID_KEY = 'id'
TWEET_RETWEET_KEY = 'retweet_count'

# special parameters to work with Twitter timelines
# https://dev.twitter.com/rest/public/timelines
TWEET_SINCE_ID = 'since_id'
TWEET_MAX_ID = 'max_id'


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
			RETWEET_THRESHOLD,
			SEARCH_API_URL,
			TWEET_TEXT_KEY,
			TWEET_ID_KEY,
			TWEET_RETWEET_KEY,
			TWEET_SINCE_ID]