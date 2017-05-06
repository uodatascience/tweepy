
#!/usr/bin/env python
# encoding: utf-8

###############
# Imports

import tweepy #https://github.com/tweepy/tweepy
import csv
import os
import re
import json

###############
# Parameters
## Twitter API credentials - fill these in with your own!
consumer_key = ""
consumer_secret = ""
access_key= ""
access_secret = ""

# Alternatively - store them in a separate file and load them so they're not hardcoded
# Path to json file with credentials
auth_loc = os.path.join(os.path.expanduser('~'),"tweepy_auth.json")

# Wrapping in a try block for now because it looks like this was intended to be run from the command line but I don't want to implement taking arguments rn
try:
    with open(auth_loc) as auth_f:
        creds = json.load(auth_f)
        auth_f.close()

        # Declares the dict as variables
        locals().update(creds)
except:
    print("Unable to load .json auth, using hardcoded creds if we can")

# Output directory to save files
out_dir = os.path.join(os.path.expanduser('~'),"tweepy_data")
if not os.path.exists(out_dir):
    os.mkdir(out_dir)

#############
# Function definitions

def authorize_tweepy():
    # authorize twitter, initialize tweepy
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)

    return api


def get_all_tweets(screen_name, api=None, save=True):
    #Twitter only allows access to a users most recent 3240 tweets with this method
    if not api:
        api = authorize_tweepy()

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

    if save:
        #write the csv
        csv_f = os.path.join(out_dir,'{}_tweets.csv'.format(screen_name))
        with open(csv_f, 'w') as f:
            writer = csv.writer(f)
            writer.writerow(["screen name","id","created_at","text"])
            writer.writerows(outtweets)
    else:
        return outtweets

def load_tweets(screen_name, just_rt=False):
    # Use just_text to return just the tweets as a list
    # Use just_rt to get only retweets

    try:
        csv_f = [f for f in os.listdir(out_dir) if screen_name in f][0]
    except:
        print("Can't find tweets for {}".format(screen_name))
        return

    with open("{}{}".format(out_dir,csvfname),"r") as f:
            tweets = []
            dict_read = csv.DictReader(f)
            for row in dict_read:
                if just_rt:
                    if "RT " in row['text']:
                        tweets.append(row['text'])
                else:
                    tweets.append(row)


if __name__ == '__main__':
    #pass in the username of the account you want to download
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


