# Chicago-Beach-Bot
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://www.gnu.org/licenses/gpl-3.0)
![Twitter URL](https://img.shields.io/twitter/url/https/ChicagoBeachBot?label=ChicagoBeachBot&style=social)

This is a Twitter bot built using Tweeply for Python. This bot works on mentions to @ChicagoBeachBot using Twitter's
streaming API. On mention, it will send a request to Chicago's SODA API (https://dev.socrata.com/foundry/data.cityofchicago.org/xvsz-3xcj)
and parse the JSON file for the requested name of the beach. It then replies to the user with the predicted daily value of CFU.
# Why?
This Summer has seen an increasing amount of beach closures due to high levels of E.Coli levels measured in colony forming units/100mL. When levels exceed 235 CFU the beach is shut down. 
The data is very easily accessible, and the City of Chicago actually provides a fairly intuitive way for people to check if a beach [is open or closed](https://www.chicagoparkdistrict.com/parks-facilities/beaches). But many people aren't aware of it as it isn't a topic that's talked about too often in the news. I created this bot with the intention of making it
easier for an average person to quickly find information on a beach using Twitter, the social platform where a bot like this actually has a use.
# How can I make one for my city?
If there is any similar data provided by your city through Socrata, most of the modifications should be in the `process_data` function. 
If Socrata isn't available but there is an API, I would suggest using the requests library and working off of that with Pandas.
The `on_status ` method is part of [Tweepy](http://docs.tweepy.org/en/latest/streaming_how_to.html), and it handles the "tweeting" functionality of the bot.
The bot focuses on using Twitter and Tweepy's streaming api rather than fetching the data periodically. In `__init__` I initialize the beaches dictionary. This is a 
dictionary of 'valid' beach names that is used in `on_status`. For a different city, you would just need to change the keys to the new beach names and attempt to account for 
the short-hand way of referencing them or for the local and unofficial names. 
