import re
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot


INFERRED_TOPICS_FILE = "inferred-topics.1"

TOPICS_PATTERN = "(\d*) null-source ([ .\d]*)\n"
TOPIC_PATTERN = "(\d*) (0\.\d*)"

NUM_TOPICS = 10


TWEET_DATA_FILE = "sample-data/tweets.txt"
TWEET_DATA_PATTERN = "twitter (\S*) (.*)"

def parse_topics():
    ''' Returns an M by N array, where M is number of tweets, N is number of topics, and A[m,n] is the value of the m'th topic for the n'th tweet. '''

    inferred_topics_string = open(INFERRED_TOPICS_FILE,'r').read()
    matches = re.findall(TOPICS_PATTERN, inferred_topics_string)

    topic_data = zeros((len(matches),NUM_TOPICS))

    for index,topics in matches:
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

    for user_index, (username,tweets) in enumerate(user_tweets.items()):
        for tweet_index in tweets:
            user_matrix[user_index,tweet_index] = 1


    return user_matrix

def main():

    topic_matrix = parse_topics()
    print(topic_matrix.shape)

    user_matrix = parse_tweets()
    print(user_matrix.shape)

if __name__ == "__main__":
    main()
