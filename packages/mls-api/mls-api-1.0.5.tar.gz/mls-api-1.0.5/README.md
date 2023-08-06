# MLS API Python Package

The package provides convenient access to the [MLS API](https://moatsystems.com/mls-api/) functionality from applications written in the Python language.

## Requirements

Python 2.7 and later.

## Setup

You can install this package by using the pip tool and installing:

```python
pip install mls-api
## OR
easy_install mls-api
```

Install from source with:

```python
python setup.py install --user

## or `sudo python setup.py install` to install the package for all users
```

Usage Example
-------------

```python
import mls_api
from dotenv import load_dotenv
import os

## Loads environment variables from .env
load_dotenv('.env')

username = os.getenv('_USERNAME')
password = os.getenv('_PASSWORD')

## Authentication
mls_api.login(username, password)

## Retrieve MLS Real-Time Data
mls_rtd = mls_api.get_rtd()
print(mls_rtd)

## Retrieve MLS Real-Time Data by ID
mls_rtd_id = mls_api.get_rtd(id='<insert unique id>')
print(mls_rtd_id)

## Retrieve MLS Historical Data
mls_historical = mls_api.get_historical_data()
print(mls_historical)

## Retrieve MLS Historical Data by ID
mls_historical_id = mls_api.get_historical_data(id='<insert unique id>')
print(mls_historical_id)

## Retrieve MLS Players Data
mls_players = mls_api.get_players()
print(mls_players)

## Retrieve MLS Players Data by ID
mls_players_id = mls_api.get_players(id='<insert unique id>')
print(mls_players_id)

## Retrieve MLS Assist Data
mls_assists = mls_api.get_assists()
print(mls_assists)

## Retrieve MLS Assist Data by ID
mls_assists_id = mls_api.get_assists(id='<insert unique id>')
print(mls_assists_id)

## Retrieve MLS Offence Data
mls_offence = mls_api.get_offence()
print(mls_offence)

## Retrieve MLS Offence Data by ID
mls_offence_id = mls_api.get_offence(id='<insert unique id>')
print(mls_offence_id)

## Retrieve MLS Top Scorers Data
mls_top_scorer = mls_api.get_top_scorer()
print(mls_top_scorer)

## Retrieve MLS Top Scorers Data by ID
mls_top_scorer_id = mls_api.get_top_scorer(id='<insert unique id>')
print(mls_top_scorer_id)

## Retrieve MLS Teams Data
mls_teams = mls_api.get_teams()
print(mls_teams)

## Retrieve MLS Teams Data by ID
mls_teams_id = mls_api.get_teams(id='<insert unique id>')
print(mls_teams_id)

## Retrieve MLS Fixtures Data
mls_fixtures = mls_api.get_fixtures()
print(mls_fixtures)

## Retrieve MLS Fixtures Data by ID
mls_fixtures_id = mls_api.get_fixtures(id='<insert unique id>')
print(mls_fixtures_id)

## Retrieve MLS Standings Data
mls_standings = mls_api.get_standings()
print(mls_standings)

## Retrieve MLS Standings Data by ID
mls_standings_id = mls_api.get_standings(id='<insert unique id>')
print(mls_standings_id)

## Retrieve MLS Latest News Data
mls_latest_news = mls_api.get_latest_news()
print(mls_latest_news)

## Retrieve MLS Latest News Data by ID
mls_latest_news_id = mls_api.get_latest_news(id='<insert unique id>')
print(mls_latest_news_id)
```

## Setting up an MLS API Account

Sign up for a self-service [user account](https://moatsystems.com/mls-api/).


## Using the MLS API

You can read the [API documentation](https://docs.mlssoccerapi.com/) to understand what's possible with the MLS API. If you need further assistance, don't hesitate to [contact us](https://moatsystems.com/contact/).


## License

This project is licensed under the [MIT License](./LICENSE).


## Copyright

(c) 2022 [Moat Systems Limited](https://moatsystems.com/). All Rights Reserved.
