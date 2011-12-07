import re
from settings import *
from utils import get_followers_count
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
import os
import simplejson as json


TOPICS_PATTERN = "(\d*) null-source ([ .\d]*)"
TOPIC_PATTERN = "(\d*) (0\.\d*)"

TWEET_DATA_FILE = "sample-data/tweets.txt"
TWEET_DATA_PATTERN = "twitter (\S*) (.*)\n"

def parse_topics():
    ''' Returns an M by N array, where M is number of tweets, N is number of topics, and A[m,n] is the value of the m'th topic for the n'th tweet. '''

    inferred_topics_string = open(INFERRED_FILE,'r').read()
    matches = re.findall(TOPICS_PATTERN, inferred_topics_string)

    topic_data = zeros((len(matches),NUM_TOPICS))

    for i,(index,topics) in enumerate(matches):
        tm = re.findall(TOPIC_PATTERN,topics)

        for topic, value in tm:
            topic_data[int(index),int(topic)] = float(value)

    return topic_data

def parse_tweets():
    tweet_file = open(TWEET_DATA_FILE,'r')
    matches = re.findall(TWEET_DATA_PATTERN, tweet_file.read())

    user_tweets = {}

    for tweet_index, (username,tweet) in enumerate(matches):
        tweets = user_tweets.get(username,[])
        tweets.append(tweet_index)
        user_tweets[username] = tweets

    user_matrix = zeros((len(user_tweets),len(matches)))

    indexed_usernames = []
    for user_index, (username,tweets) in enumerate(user_tweets.items()):
        indexed_usernames.append(username)
        for tweet_index in tweets:
            user_matrix[user_index,tweet_index] = 1


    return user_matrix, indexed_usernames

def get_user_metadata(indexed_usernames):
    user_metadata_matrix = zeros((len(indexed_usernames),2))

    for i, username in enumerate(indexed_usernames):
        log_name = "%s%s.json"%(LOG_PATH,username) 
        if os.path.isfile(log_name):
            log = json.loads(open(log_name,'r').read())
            user_metadata_matrix[i,0] = log[0]['user']['followers_count']
            user_metadata_matrix[i,1] = log[0]['user']['friends_count']

    return user_metadata_matrix

def main():

    print "Starting to prepare data"

    user_tweet_matrix, indexed_usernames = parse_tweets()
    numpy.save('user_tweet_matrix', user_tweet_matrix)
    print "Saved user_tweet_matrix"

    user_metadata_matrix = get_user_metadata(indexed_usernames)
    numpy.save('user_metadata_matrix', user_metadata_matrix)
    print user_metadata_matrix
    print "Saved user_metadata_matrix"

    tweet_topic_matrix = parse_topics()
    numpy.save('tweet_topic_matrix',tweet_topic_matrix)
    print "Saved tweet_topic_matrix"

    user_topic_matrix = dot(user_tweet_matrix,tweet_topic_matrix)
    numpy.save('user_topic_matrix',user_topic_matrix)
    print "Saved user_topic_matrix"

if __name__ == "__main__":
    main()
