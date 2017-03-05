import tweepy, time, sys
from SListener import SListener
import json

auth = tweepy.OAuthHandler('CdmceagVFZra8OR58OyP9FglK', 'qNg9qyQpM2SbQglmxg0Rvfrwozh9r4S82zYDwV4fS2ur7tAVWd')
auth.set_access_token('612123054-irckztQDF42DdcCBHkmcnFa8ADc7QrL21wsb7xRY', 'QKRa2AAX2CrUF0VxmE9ypeoQEYI9IfZgAHzS6YHGlnUS3')

api = tweepy.API(auth)


def main():
	track = ['ndmbb', "Notre Dame Men's Basketball", 'Mike Brey', '@NDMikeBrey', 'Bonzie Colson', '@BonzieColson', 'Matt Farrell', '@MattyFarr3', 'Austin Torres', '@Austin_Torres0', 'VJ Beachem', '@VjBeachem', 'Patrick Mazza', '@P_Mazz', 'John Mooney', '@jmoon32', 'Nikola Djogo', '@NikolaDjogo', 'TJ Gibbs', '@Tempppp12', 'Elijah Burns', '@ElijahBurns12', '@Matt_Ryan04', 'Rex Pflueger', '@rexpflueger_1' 'Martinas Geben', '@Martin_Geben', '#BCEagles', '@BCEagles', "Boston College Men's Basketball", 'bcmbb', "BC Men's Basketball", 'Ky Bowman', 'Jerome Robinson', '@rome_coldbucks3', 'Boston College Basketball', 'Connar Tava', '@megacon_2', 'Garland Owens', '@Owens_5', 'Ervins Meznieks', 'A.J. Turner', 'Johncarlos Reyes', '@JayCee809', 'Aser Ghebremichael', 'Mo Jeffers', 'Gordon Gehan', 'Nik Popovic', 'Matt DeLuccio', 'Mike Sagay', '@MSJXXIII', 'Jordan Chatman', 'Jim Christian']

	listen = SListener(api, 'bc_301')
	stream = tweepy.Stream(auth, listen)

	print "Streaming started..."

	try:
		stream.filter(track = track)
	except:
		print "error!"
		stream.disconnect()

if __name__ == '__main__':
	main()



