import tweepy
import pandas as pd
from random import randrange
from sodapy import Socrata
from os import environ

#used for heroku deployment
CONSUMER_KEY = environ['CONSUMER_KEY']
CONSUMER_SECRET = environ['CONSUMER_SECRET']
ACCESS_KEY = environ['ACCESS_KEY']
ACCESS_SECRET = environ['ACCESS_SECRET']

# authenticate to twitter
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

# create API object
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)


class MyStreamListener(tweepy.StreamListener):
	def __init__(self, api):
		self.api = api
		self.user = api.me()

		self.status = ''
		self.predicted_level = 0
		self.beach_to_parse = ''
		self.jsonData = []
		self.tweet = []

		self.beaches = {
			'12th': self.get_data, '12': self.get_data, '31st': self.get_data,
			'57th':self.get_data, '57':self.get_data, 'albion':self.get_data,
			'foster': self.get_data, 'hartigan':self.get_data, 'howard':self.get_data, 'jarvis':self.get_data,
			'juneway':self.get_data, 'leone': self.get_data, 'margaret t burroughs': self.get_data, 'marion mahogany griffin':self.get_data,
			'montrose': self.get_data, 'north':self.get_data, 'north avenue':self.get_data, 'oak': self.get_data,
			'oak street': self.get_data, 'oakwood':self.get_data, 'ohio': self.get_data,
			'osterman': self.get_data, 'rogers': self.get_data
		}

	def listen(self):
		print(self.user.screen_name)
		tweets_listener = MyStreamListener(api)
		stream = tweepy.Stream(api.auth, tweets_listener)
		stream.filter(track=["@ChicagoBeachBot"], languages=["en"])

	def on_status(self, status):
		tag_number = randrange(1, 10)   # used to prevent duplicate tweet error
		list_of_names = list(self.beaches.keys())
		replied = False     # breaks the loop to prevent infinite replies
		found = True

		self.tweet = status.text.lower().split()
		print(self.tweet)

		while not replied:
			for word in self.tweet[1:]:  # ignores the mention
				if word in list_of_names:
					self.beach_to_parse = word.capitalize()
					self.get_data()
					if float(self.predicted_level) <= 180:
						self.status = 'good'
						api.update_status(
							" {} is {}. It's predicted to be at {} today where {} is the cutoff.  #{}".
								format(self.beach_to_parse, self.status, self.predicted_level, 235, tag_number),
							in_reply_to_status_id=status.id, auto_populate_reply_metadata = True
						)
						replied, found = True, True
					elif float(self.predicted_level) <= 220:
						self.status = "on the edge today"
						api.update_status(
							" {} is {}. It's predicted to be at {} where {} is the cutoff.  #{}".
								format(self.beach_to_parse, self.status, self.predicted_level, 235, tag_number),
							in_reply_to_status_id=status.id, auto_populate_reply_metadata = True
						)
						replied, found = True, True
					elif float(self.predicted_level) >= 235:
						self.status = "dangerous. It should be closed."
						api.update_status(
							" {} is {}. It's predicted to be at {} today where {} is the cutoff.  #{}".
								format(self.beach_to_parse, self.status, self.predicted_level, 235, tag_number),
							in_reply_to_status_id=status.id, auto_populate_reply_metadata = True
						)
						replied, found = True, True
			if not found:
				api.update_status(
					"ERROR! ERROR!"
					"I wasn't able to find a valid beach name, if you didn't make a typo I must not have it. Sorry :(",
					in_reply_to_status_id=status.id, auto_populate_reply_metadata=True
				)
				replied = True

	def on_error(self, status):
		print("Error detected")

	def get_data(self):
		print('SUCCESS')
		print('Collecting data...')
		self.process_data(self.beach_to_parse)

	def process_data(self, searchTerm):
		client = Socrata("data.cityofchicago.org", None)
		self.jsonData = client.get('xvsz-3xcj', limit=15, content_type='JSON')
		print(self.jsonData, end = '\n')
		data_frame = pd.DataFrame.from_records(self.jsonData)
		data_frame = data_frame.set_index('beach_name') #set row labels to names
		data_frame = data_frame[['predicted_level', 'recordid']] #gives df with names as row labels and values
		print(data_frame)
		selection = data_frame[data_frame.index.str.contains(searchTerm)]
		print(selection)
		self.predicted_level = selection['predicted_level'].iloc[0]
		print(self.predicted_level)

t = MyStreamListener(api)
t.listen()
