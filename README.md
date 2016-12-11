# hearthstone

Python 3 tools for studying Hearthstone cards. Data is provided by a [third-party API](http://hearthstoneapi.com/) hosted on [Mashape](https://market.mashape.com/omgvamp/hearthstone).

### Quickstart

Create a `settings.yml` file at the root of the repo and put your Mashape application key in it. See `settings.yml.example` for an example of what this file should look like. See the [Mashape docs](http://docs.mashape.com/api-keys) for instructions on getting API keys.

After creating a Python 3 virtualenv, install requirements:

```
$ make requirements
```

Pull data from the API and save it to the `data` directory:

```
$ make load
```

Open the included Jupyter notebook:

```
$ make explore
```
