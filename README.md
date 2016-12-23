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

