import tweepy
from tweepy import StreamListener
import json, time, sys, re, string, copy
from nltk.corpus import stopwords
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
from tweepy.api import API



regex = re.compile('[%s]' % re.escape(string.punctuation))
cachedStopWords = stopwords.words('english')

class SListener(StreamListener):

	def __init__(self, home_words, away_words, api = None):
		self.api = api or API()
		self.analyzer = SentimentIntensityAnalyzer()
		self.counter = 0
		self.max = 1000000000
		self.home_words = set(home_words.values())
		self.away_words = set(away_words.values())
		self.tweetTeams={}

		self.total_neg_home = 0
		self.total_pos_home = 0
		self.total_neg_away = 0
		self.total_pos_away = 0
		
		self.home_score = 0
		self.away_score = 0



	def on_status(self, status):
	
		tweet = status.text.encode('utf8')
		vs = self.analyzer.polarity_scores(tweet)
		print("{:-<65} {}".format(tweet, str(vs)))
		sent = vs['compound']		

		team = self.classifyTweet(tweet)

		#update scores
		if team=="home":
			if sent > 0:
				self.total_pos_home += sent
				#print "positive home ",self.total_pos_home
			elif sent < 0:
				self.total_neg_home -= sent
				#print "negative home ", self.total_neg_home
		elif team=="away":
			if sent > 0:
				self.total_pos_away += sent
				#print "positive away ", self.total_pos_away
			elif sent < 0:
				self.total_neg_away -= sent
				#print "negative away ", self.total_neg_away

		self.decideWinner()

		self.counter += 1
		if self.counter < self.max: return True
		else:
			return False

	def on_error(self, status_code):
		sys.stderr.write('Error: ' + str(status_code) + "\n")
		time.sleep(60)
		return

	def wordSet(self, string):
		words = string.lower().strip().split(' ')
		for word in words:
			word = word.rstrip().lstrip()
			if not re.match(r'^https?;\/\/.*[\r\n]*', word) \
			and not re.match('^@.*', word) \
			and not re.match('\s', word) \
			and word not in cachedStopWords \
			and word != 'rt' \
			and word != ' ':
				yield regex.sub(' ', word)

	def jaccardDist(self, A, B):
		jaccDist = 1 - float(len(A.intersection(B))) / float(len(A.union(B)))
                return jaccDist

	def classifyTweet(self,tweet):
		tweet_words = set(self.wordSet(tweet))


		#grab words from home and away lists
		distHome = self.jaccardDist(tweet_words, self.home_words)
		distAway = self.jaccardDist(tweet_words, self.away_words)

		if distHome < distAway:
			self.tweetTeams[tweet] = "home"
			return self.tweetTeams[tweet]
		elif distHome > distAway:
			self.tweetTeams[tweet] = "away"
			return self.tweetTeams[tweet]

	def decideWinner(self):
		total_home = self.total_pos_home + self.total_neg_home
		total_away = self.total_pos_away + self.total_neg_away

		if total_home != 0:
#			print "self.total_pos_home ", self.total_pos_home
			self.total_home = (float(self.total_pos_home)/float(total_home)) * 100
		else:
			self.total_home = 0

		if total_away != 0:
#			print "self.total_pos_away ", self.total_pos_away
			self.total_away = (self.total_pos_away/total_away) * 100
		else:
			self.total_away = 0

		print "Home Positive Percentage", self.total_home
                print "Away Positive Percentage", self.total_away

                if self.total_home> self.total_away:
                        print "HOME TEAM WINNING"
                elif self.total_away > self.total_home:
                        print "AWAY TEAM WINNING"

		print "\n"
