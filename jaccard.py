import sys
import json
import re, string
import copy
from nltk.corpus import stopwords
<<<<<<< HEAD
=======
import matplotlib.pyplot as plt
import matplotlib.cm as cm

>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d

#method to strip punctuation from incoming strings and return list of lowercase stop words ('the', 'is', 'at', etc)
regex = re.compile('[%s]' % re.escape(string.punctuation))
cachedStopWords = stopwords.words('english')

<<<<<<< HEAD
=======

>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
class Jaccard():
	def __init__(self, tweets, pos_words, neg_words, home_team_words, away_team_words):
		self.tweets = tweets
		self.pos_words = pos_words
		self.neg_words = neg_words
		self.home_team_words = home_team_words
		self.away_team_words = away_team_words
		self.jaccardMatrix = {} 
		self.tweetTeams = {}
		self.total_neg_home =0
		self.total_neg_away = 0
		self.total_pos_away = 0
		self.total_pos_home = 0
		self.total_home = 0
		self.total_away = 0
<<<<<<< HEAD
		self.t = 0
=======
		self.graph = 0
>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
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
			print "words from tweet: ", words1

			#grab second set of words from second tweet
			words2 = set(self.home_team_words.values())
			words3 = set(self.away_team_words.values())

			#calculate Jaccard distance b/t two sets of words & update Jaccard 2D matrix
			distanceHome = self.jaccardDist(words1, words2)
			print "distanceHome= ", distanceHome
			distanceAway = self.jaccardDist(words1, words3)
			print "distanceAway= ", distanceAway
			if distanceHome < distanceAway:
				self.tweetTeams[tweet1] = "home"
				print "new home tweet"
			elif distanceHome > distanceAway:
				self.tweetTeams[tweet1] = "away"
				print "new away tweet"
			
	

	def printMatrix(self):
		#prints Jaccard Distance matrix
		for tweet in self.tweets:
			print tweet, "positive Jaccard: ", self.jaccardMatrix[tweet][0]
			print tweet, "negative Jaccard: ", self.jaccardMatrix[tweet][1]

	def decideSentiment(self):
		#depending which distance is shorter, decide if tweet is positive or negative
<<<<<<< HEAD
=======
		i = 0

>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
		for tweet in self.tweets:
			if self.jaccardMatrix[tweet][0] > self.jaccardMatrix[tweet][1]:
				#print self.tweets[tweet]['text'].encode('ascii', 'ignore'), " is negative"
				if self.tweetTeams[tweet] == "home":
					self.home_score = self.home_score - 1
					print "home score: ", self.home_score
					self.total_neg_home += 1
<<<<<<< HEAD
=======
					self.total_home = (self.total_pos_home * 100)/(self.total_pos_home + self.total_neg_home)
					self.graph = self.total_home - self.total_away

					i += 1
					plt.xlabel('Tweets (As game progresses)')
					plt.ylabel('Difference in Positive Percentage\n\nAway                                             Home')

					plt.title("Notre Dame vs Georgia Tech (02-26-2017)")
					#plt.axis([0,i,-50,50])    #For more detailed look
					plt.scatter(i,self.graph)
					plt.pause(.001)
>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
				
				elif self.tweetTeams[tweet] == "away":
					self.away_score = self.away_score - 1
					print "away score: ", self.away_score
					self.total_neg_away +=1
<<<<<<< HEAD

=======
					self.total_away = (self.total_pos_away * 100)/(self.total_pos_away + self.total_neg_away)
					self.graph = self.total_home - self.total_away
					i += 1

					plt.scatter(i,self.graph)
					plt.plot(i, self.graph)
					
					plt.pause(.001)
						
>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
			elif self.jaccardMatrix[tweet][0] < self.jaccardMatrix[tweet][1]:
				#print self.tweets[tweet]['text'].encode('ascii', 'ignore'), " is positive"
				if self.tweetTeams[tweet] == "home":
					self.home_score = self.home_score + 1
					print "home score: ", self.home_score
					self.total_pos_home += 1
<<<<<<< HEAD
=======
					self.total_home = (self.total_pos_home * 100)/(self.total_pos_home + self.total_neg_home)
					self.graph = self.total_home - self.total_away

					i += 1
					
					plt.scatter(i,self.graph)
					plt.plot(i,self.graph)
					plt.pause(.001)
				
>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
				elif self.tweetTeams[tweet] == "away":
					self.away_score = self.away_score + 1
					print "away score: ", self.away_score
					self.total_pos_away += 1
<<<<<<< HEAD

=======
					self.total_away = (self.total_pos_away * 100)/(self.total_pos_away + self.total_neg_away)
					self.graph = self.total_home - self.total_away

					i += 1
					plt.scatter(i,self.graph)
					plt.plot(i,self.graph)
					plt.pause(.001)
>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
	def decideWinner(self):
		
		self.total_home = (self.total_pos_home * 100)/(self.total_pos_home + self.total_neg_home)
		self.total_away = (self.total_pos_away * 100)/(self.total_pos_away + self.total_neg_away)


		print "Home Score: ", self.home_score
		print "Away Score: ", self.away_score
		
		print "Home Positive Percentage", self.total_home
		print "Away Positive Percentage", self.total_away
		
		if self.home_score >= self.away_score:
			print "HOME TEAM WON"
		elif self.away_score > self.home_score:
			print "AWAY TEAM WON"

if __name__ == '__main__':
	if len(sys.argv) != 6:
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

	home_words = {}
	i=0
	with open(sys.argv[4], 'r') as file:
		for line in file:
			home_words[i]=line.rstrip('\n')
			i=i+1	
	
	away_words = {}
	i=0
	with open(sys.argv[5], 'r') as file:
		for line in file:
			away_words[i]=line.rstrip('\n')
			i=i+1	

	jaccard = Jaccard(tweets, pos_words, neg_words, home_words, away_words)
	jaccard.initializeTeams()
	#jaccard.printMatrix()
	jaccard.decideSentiment()
	jaccard.decideWinner()
<<<<<<< HEAD
=======
	plt.show()
>>>>>>> 90b164745f1408bfd301efc5ab6b088a36bba45d
