#!/usr/bin/python
import tweepy
from pprint import pprint
import argparse, os, time, json, csv


#Create class override for stream listener
class MyStreamListener(tweepy.StreamListener):

	def on_status(self, status):
		print(status.text)


'''
This block sets up our authentication. The keys/secrets should NOT be stored in plain text in this script.
Will be setting up environment variables to prevent this later.
'''
def set_creds():
	consumer_key = os.getenv('consumer_key')
	consumer_secret = os.getenv('consumer_secret')
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	key = os.getenv('key')
	secret = os.getenv('secret')
	auth.set_access_token(key, secret)
	api = tweepy.API(auth)
	return api

def stream_setup():
	api = set_creds()
	myStreamListener = MyStreamListener()
	myStream = tweepy.Stream(auth = api.auth, listener=myStreamListener)
	return myStream

def stream_follow(key_word, thread=False):
	#insert code to parse cli options for thread var, assume false otherwise and initially
	my_stream = stream_setup()
	my_stream.filter(track=[key_word])

def parse_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("-k", "--key-word", help="the keyword to filter for", action="store", dest="key_word")
	parser.add_argument("-t", "--thread", help="runs the stream on a sub-thread (will be more useful when I figure out sub-threading)", action="store_true", default=False, dest="thread")

	results = parser.parse_args()
	#We always want a keyword
	if results.key_word:
		stream_follow(results.key_word)
	else:
		parser.print_help()

parse_arguments()