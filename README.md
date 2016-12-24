# kayak
A customizable Twitter client to collect tweets matching certain criteria

## Setting up kayak

### Twitter Application Credentials

* Create a new application using [Twitter Application Management](https://apps.twitter.com/) console.
* Note down the *Consumer Key (API Key)* and *Consumer Secret (API Secret)* credentials.

###### [Optional] Application's **Access Level** should be **Read only**.

### Store Credentials as Environment Variables

* Save the consumer key and consumer secret credentials as envrionment variables titled *KAYAK_CONSUMER_KEY* and *KAYAK_CONSUMER_SECRET* respectively.
* One possible way to add environment variables is to add them to your *~/.bashrc* file and *source* it.

```bash
KAYAK_CONSUMER_KEY="xxxxxxxx"; export KAYAK_CONSUMER_KEY
KAYAK_CONSUMER_SECRET="xxxxxxxxxxxxxxxx"; export KAYAK_CONSUMER_SECRET
```

### Installation

For now the package isn't up there on PyPI, hence you'll have to install it manually.

```bash
$ git clone git@github.com:pravj/kayak.git
$ cd kayak
$ pip install .
```

It will make the package available in your local environment.

--

## Using kayak

The package exports **KayakClient** class to use, it defines the following method.

```
get_tweets(search_query, minimum_retweet=1, older_tweets=True)
    Returns an iterator for Twitter API responses (tweet entities i.e. KayakTweet).

    :param (str) search_query: Search query operator to use.

    :param (int) minimum_retweet: Number of retweets (Default 1)
        a tweet should have at least.

    :param (bool) older_tweets:
        If True (default), it will return the iterator with older tweets.
        If False, it will return newer tweets on each iteration.
```

The class **KayakTweet** provides following variables of a tweet.

* **text** : Tweet text
* **id** : ID of the Tweet
* **retweets** : Number of retweets

```
class KayakTweet(object):
    """
    Class to change the representation of a Tweet object.
    Currently you can access the 'text', 'id', and 'retweet count' attributes.
    """
```

--

Create a client instance.

```python
from kayak import KayakClient

client = KayakClient()
```

###### Refer to the API documentation [Query operators](https://dev.twitter.com/rest/public/search) to create your custom search query.

### To collect old tweets (that have been created in past)

```python
search_query = '#custserv'

# Similarly, if you want tweets mentioning Twitter account '@potus'
# search_query = '@potus'

old_tweets_iterator = client.get_tweets(search_query, minimum_retweet=2)

for tweets in old_tweets_iterator:
	for tweet in tweets:
		print tweet.id, tweet.retweets

		# same value (str) as 'tweet.text' (using __repr__ data method)
		print tweet
```

### To collect new tweets (as they are being created continuously)

```python
# Ideally, to avoid raising Exception
# one should wait in between successive iterations.
# So that we don't end up having no new tweets.
import time

new_tweets_iterator = client.get_tweets('#custserv', older_tweets=False)

while True:
	new_tweets = new_tweets_iterator.next()

	for tweet in new_tweets:
		print tweet.id, tweet.retweets
		print tweet.text

	time.sleep(60)
```

### Tweet Filteration

#### Custom Filter Function

[TODO](https://github.com/pravj/kayak/blob/master/TODO.md)

--

## LICENSE

[Pravendra Singh](http://pravj.github.io) • GPLv3