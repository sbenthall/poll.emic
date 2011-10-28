import re
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
from math import log
import matplotlib.pyplot as pyplot


INFERRED_TOPICS_FILE = "inferred-topics.1"

TOPICS_PATTERN = "(\d*) null-source ([ .\d]*)\n"
TOPIC_PATTERN = "(\d*) (0\.\d*)"

NUM_TOPICS = 100


TWEET_DATA_FILE = "sample-data/tweets.txt"
TWEET_DATA_PATTERN = "twitter (\S*) (.*)\n"

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

def normalize(dist):
    total = sum(dist)
    return dist / total

def entropy(dist):
    return 0 - sum([p * log(p) for p in normalize(dist)])

def main():

    topic_matrix = parse_topics()
    print(topic_matrix.shape)

    user_matrix = parse_tweets()
    print(user_matrix.shape)

    x_matrix = dot(user_matrix,topic_matrix)
    print(x_matrix.shape)

    entropies = [entropy(x_matrix[i,:]) for i in range(x_matrix.shape[0])]

    print(entropies)

    # the histogram of the data
    n, bins, patches = pyplot.hist(entropies, 50)
    print(n, bins, patches)
    pyplot.title("Entropy Histogram")
    pyplot.savefig("histogram.png", format='png')

    #pyplot.scatter(x_matrix[0,:],x_matrix[1,:])


if __name__ == "__main__":
    main()
