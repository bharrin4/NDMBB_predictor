import tweepy, time, sys
from SportsListener import SportsListener
import json
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

auth = tweepy.OAuthHandler('CdmceagVFZra8OR58OyP9FglK', 'qNg9qyQpM2SbQglmxg0Rvfrwozh9r4S82zYDwV4fS2ur7tAVWd')
auth.set_access_token('612123054-irckztQDF42DdcCBHkmcnFa8ADc7QrL21wsb7xRY', 'QKRa2AAX2CrUF0VxmE9ypeoQEYI9IfZgAHzS6YHGlnUS3')

api = tweepy.API(auth)


def main():

	if len(sys.argv) != 3:
		print "incorrect number of arguments"
		exit(-1)

	#read teets from positive and negative files
	home_words = {}
	i = 0
	with open(sys.argv[1], 'r') as file:
		for line in file:
			home_words[i] = line.rstrip('\n')
			i=i+1
	away_words = {}
	i = 0
	with open(sys.argv[2], 'r') as file:
		for line in file:
			away_words[i] = line.rstrip('\n')
			i=i+1
	 
	
	track = home_words.values() + away_words.values()


	listen = SportsListener(home_words, away_words, api)
	stream = tweepy.Stream(auth, listen)

	print "Streaming started..."

	try:
		stream.filter(track = track)
	except:
		print "error!"
		stream.disconnect()

if __name__ == '__main__':
	main()



