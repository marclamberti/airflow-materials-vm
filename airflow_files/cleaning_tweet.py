import pandas as pd
import numpy as np
import re
from datetime import datetime as dt
from datetime import date, timedelta

# This script cleans the fetched tweets from the previous task "fetching_tweets"

LOCAL_DIR='/tmp/'

def main():
	# Read the csv produced by the "fetching_tweets" task
	tweets = pd.read_csv(LOCAL_DIR + 'data_fetched.csv')
	
	# Rename the columns of the dataframe
	tweets.rename(columns={'Tweet': 'tweet', 'Time':'dt', 'Retweet from': 'retweet_from', 'User':'tweet_user'}, inplace=True)
	
	# Drop the useless column "User" since all the tweets are written by Elon Musk
	tweets.drop(['tweet_user'], axis=1, inplace=True)
	
	# Add a column before_clean_len to know the size of the tweets before cleaning
	tweets['before_clean_len'] = [len(t) for t in tweets.tweet]
	
	# Remove @mention in tweets
	tweets['tweet'] = tweets['tweet'].apply(lambda tweet: re.sub(r'@[A-Za-z0-9]+', '', tweet))
	
	# Remove URL in tweets
	tweets['tweet'] = tweets['tweet'].apply(lambda tweet: re.sub('https?://[A-Za-z0-9./]+', '', tweet))
	
	# Remove all non letter charaters including numbers from the tweets
	tweets['tweet'] = tweets['tweet'].apply(lambda tweet: re.sub('[^a-zA-Z]', ' ', tweet))
	
	# Lower case all the tweets
	tweets['tweet'] = tweets['tweet'].str.lower()
	
	# Add after clean len column
	tweets['after_clean_len'] = [len(t) for t in tweets.tweet]
	
	# Changing date format
	yesterday = date.today() - timedelta(days=1)
	dt = yesterday.strftime("%Y-%m-%d")
	tweets['dt'] = dt	

	# Export cleaned dataframe
	tweets.to_csv(LOCAL_DIR + 'data_cleaned.csv', index=False)

if __name__ == '__main__':

	main()
