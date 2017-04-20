
#!/usr/bin/env python
# encoding: utf-8

import tweepy #https://github.com/tweepy/tweepy
import csv

#Twitter API credentials - fill these in with your own!
consumer_key = ""
consumer_secret = ""
access_key= ""
access_secret = ""


def get_all_tweets(screen_name):
	#Twitter only allows access to a users most recent 3240 tweets with this method
	
	#authorize twitter, initialize tweepy
	auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
	auth.set_access_token(access_key, access_secret)
	api = tweepy.API(auth)
	
	#initialize a list to hold all the tweepy Tweets
	alltweets = []	
	
	#make initial request for most recent tweets (200 is the maximum allowed count)
	new_tweets = api.user_timeline(screen_name = screen_name,count=200,wait_on_rate_limit=True,wait_on_rate_limit_notify=True) 
	
	#save most recent tweets
	alltweets.extend(new_tweets)
	
	#save the id of the oldest tweet less one
	oldest = alltweets[-1].id - 1
	
	#keep grabbing tweets until there are no tweets left to grab
	while len(new_tweets) > 0:
		print ("getting tweets before %s" % (oldest))
		
		#all subsiquent requests use the max_id param to prevent duplicates
		new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
		
		#save most recent tweets
		alltweets.extend(new_tweets)
		
		#update the id of the oldest tweet less one
		oldest = alltweets[-1].id - 1
		
		print ("...%s tweets downloaded so far" % (len(alltweets)))
	
	#transform the tweepy tweets into a 2D array that will populate the csv	
	outtweets = [[tweet.user.screen_name, tweet.id_str, tweet.created_at, tweet.text.encode("utf-8")] for tweet in alltweets]
	
	#write the csv	
	with open('%s_tweets.csv' % screen_name, 'w') as f:
		writer = csv.writer(f)
		writer.writerow(["screen name","id","created_at","text"])
		writer.writerows(outtweets)
	
	pass


if __name__ == '__main__':
	#pass in the username of the account you want to download
	get_all_tweets("realDonaldTrump")


names = "realDonaldTrump"
get_all_tweets("realDonaldTrump")


        
## get user data (probably need to reauthenticate first)
# Open/Create a file to append data
csvFile = open('ID.csv', 'a')
#Use csv Writer
csvWriter = csv.writer(csvFile)

for x in names:
    user = api.get_user(screen_name = x,wait_on_rate_limit=True)
    csvWriter.writerow([user.screen_name, user.id, user.followers_count,user.friends_count, user.statuses_count, user.created_at])
    print (user.screen_name)

csvWriter.writerow(["screen_name","user_id","followers_count","friends_count","tweet_count","created_at"])

csvFile.close()
   

