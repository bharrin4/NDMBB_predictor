from tweepy import StreamListener
import json, time, sys
import jaccard
import re, string


jaccard.Jaccard

class SListener(StreamListener):

	def __init__(self, api = None, fprefix = 'streamer'):
		self.api = api or API()
		self.counter = 0
		self.fprefix = fprefix
		self.output  = open(fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')
		self.delout  = open('delete.txt', 'a')
		self.outputScore  = open('score.txt', 'w')

	def on_data(self, data):
		if 'in_reply_to_status' in data:
			self.on_status(data)
		elif 'delete' in data:
			delete = json.loads(data)['delete']['status']
			if self.on_delete(delete['id'], delete['user_id']) is False:
				return False

		elif 'limit' in data:
			if self.on_limit(json.loads(data)['limit']['track']) is False:
				return False
		elif 'warning' in data:
			warning = json.loads(data)['warnings']
			print warning['message']
			return false

	def on_status(self, status):
		self.output.write(status + "\n")

		self.counter += 1
		
		if self.counter >= 20000:

			self.output.close()
			self.output = open('../streaming_data/' + self.fprefix + '.' + time.strftime('%Y%m%d-%H%M%S') + '.json', 'w')

			self.counter = 0

		while self.output != " ":
	
			tweets = {}
			lines = (line.rstrip() for line in self.output)
			lines = (line for line in lines if line)
			
			for line in lines:
				tweet = json.loads(line)
				tweets[tweet['id']]= tweet


		jaccard = Jaccard(tweets, pos_words, neg_words, home_words, away_words)
		jaccard.initializeTeams()
		#jaccard.printMatrix()
		jaccard.decideSentiment()
		jaccard.decideWinner()
		return

	def on_delete(self, status_id, user_id):
		self.delout.write( str(status_id) + "\n")
		return

	def on_error(self, status_code):
		sys.stderr.write('Error: ' + str(status_code) + "\n")
		time.sleep(60)
		return


