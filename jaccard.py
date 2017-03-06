import sys
import json
import re, string
import copy
from nltk.corpus import stopwords

#method to strip punctuation from incoming strings and return list of lowercase stop words ('the', 'is', 'at', etc)
regex = re.compile('[%s]' % re.escape(string.punctuation))
cachedStopWords = stopwords.words('english')

class Jaccard():
	def __init__(self, tweets, pos_words, neg_words):
		self.tweets = tweets
		self.pos_words = pos_words
		self.neg_words = neg_words
		self.home_team_words = home_team_words
		self.away_team_words = away_team_words
		self.jaccardMatrix = {} 
		self.tweetTeams = {}
		self.home_score = 0
		self.away_score = 0

		self.initializeMatrix()

	def wordSet(self, string):
		#returns set of words parsed from a given string
		#gets rid of spaces and punctuation
		#turns words lowercase
		#removes url, stop words, tweet @ and 'rt'
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
		#calculate Jaccard distance b/t two sets of tweet text
		#print "intersection: ", A.intersection(B)
		jaccDist = 1 - float(len(A.intersection(B))) / float(len(A.union(B)))
		return jaccDist

	def initializeMatrix(self):
		#Dynamic Programming: creates matrix storing jaccard distances for each pair of tweets
		for tweet1 in self.tweets:
			self.jaccardMatrix[tweet1] = {}
			
			#grab set of words from first tweet
			words1 = set(self.wordSet(self.tweets[tweet1]['text']))

			#grab second set of words from second tweet
			words2 = set(self.pos_words.values())
			words3 = set(self.neg_words.values())

			#calculate Jaccard distance b/t two sets of words & update Jaccard 2D matrix
			distancePos = self.jaccardDist(words1, words2)
			distanceNeg = self.jaccardDist(words1, words3)
			self.jaccardMatrix[tweet1][0] = distancePos
			self.jaccardMatrix[tweet1][1] = distanceNeg

	def initializeTeams(self):
		#Dynamic Programming: creates matrix storing jaccard distances for each pair of tweets
		for tweet1 in self.tweets:
			self.tweetTeams[tweet1] = ""
			
			#grab set of words from first tweet
			words1 = set(self.wordSet(self.tweets[tweet1]['text']))

			#grab second set of words from second tweet
			words2 = set(self.home_team_words.values())
			words3 = set(self.away_team_words.values())

			#calculate Jaccard distance b/t two sets of words & update Jaccard 2D matrix
			distanceHome = self.jaccardDist(words1, words2)
			distanceAway = self.jaccardDist(words1, words3)
			if distanceHome >= distanceAway:
				self.tweetTeams[tweet1] = "home"
			elif distanceHome < distanceAway:
				self.twetTeams[tweet1] = "away"
			
	

	def printMatrix(self):
		#prints Jaccard Distance matrix
		for tweet in self.tweets:
			print tweet, "positive Jaccard: ", self.jaccardMatrix[tweet][0]
			print tweet, "negative Jaccard: ", self.jaccardMatrix[tweet][1]

	def decideSentiment(self):
		#depending which distance is shorter, decide if tweet is positive or negative
		for tweet in self.tweets:
			if self.jaccardMatrix[tweet][0] > self.jaccardMatrix[tweet][1]:
				print self.tweets[tweet]['text'].encode('utf-8'), " is negative"
				if self.tweetTeams == "home":
					home_score++
				elif self.tweetTeams == "away":
					away_score++
			elif self.jaccardMatrix[tweet][0] < self.jaccardMatrix[tweet][1]:
				print self.tweets[tweet]['text'].encode('utf-8'), " is positive"
				if self.tweetTeams == "home":
					home_score--
				elif self.tweetTeams == "away":
					away_score--

if __name__ == '__main__':
	if len(sys.argv) != 4:
		print 'Incorrect number of arguments'
		exit(-1)
	
	#read tweets from json file
	tweets = {}
	with open(sys.argv[1], 'r') as file:
		lines = (line.rstrip() for line in file)
		lines = (line for line in lines if line)

		for line in lines:
			tweet = json.loads(line)
			tweets[tweet['id']]= tweet
	
	pos_words = {}
	i=0
	with open(sys.argv[2], 'r') as file:
		for line in file:
			pos_words[i]=line.rstrip('\n')
			i=i+1	
	
	neg_words = {}
	i=0
	with open(sys.argv[3], 'r') as file:
		for line in file:
			neg_words[i]=line.rstrip('\n')
			i=i+1	

	jaccard = Jaccard(tweets, pos_words, neg_words)
	jaccard.printMatrix()
	jaccard.decideSentiment()

