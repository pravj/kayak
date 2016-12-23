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
get_tweets(self, older_tweets=True)
    Returns an iterator for Twitter API responses (tweet entities).
      
    :param (bool) older_tweets:
    If True (default), it will return the iterator containing older tweets.
    If False, it will return newer tweets on each iteration.
```

Create a client instance.

```python
from kayak import KayakClient

client = KayakClient()
```

### To collect old tweets (that have been created in past)

```python
old_tweets_iterator = client.get_tweets()

for tweets in old_tweets_iterator:
	for tweet in tweets:
		print tweet.id, tweet.retweets

		# same value (str) as 'tweet.text' (using __repr__ data method)
		print tweet
```

### To collect new tweets (as they are being created continuously)

```python
import time

new_tweets_iterator = client.get_tweets(older_tweets=False)

# Ideally, to avoid raising Exception
# one should wait in between successive iterations
# so that we don't end up having no new tweets.

while True:
	new_tweets = new_tweets_iterator.next()

	for tweet in new_tweets:
		print tweet.id, tweet.retweets
		print tweet.text

	time.sleep(60)
```

--

## LICENSE

[Pravendra Singh](http://pravj.github.io) • GPLv3