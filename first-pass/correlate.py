import re
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
from math import log
import matplotlib.pyplot as pyplot
import os
import simplejson as json
from pylab import axes, axis

INFERRED_TOPICS_FILE = "inferred-topics.1"

TOPICS_PATTERN = "(\d*) null-source ([ .\d]*)\n"
TOPIC_PATTERN = "(\d*) (0\.\d*)"

NUM_TOPICS = 100


TWEET_DATA_FILE = "sample-data/tweets.txt"
TWEET_DATA_PATTERN = "twitter (\S*) (.*)\n"

LOG_PATH = "log/"

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

    indexed_usernames = []
    for user_index, (username,tweets) in enumerate(user_tweets.items()):
        indexed_usernames.append(username)
        for tweet_index in tweets:
            user_matrix[user_index,tweet_index] = 1


    return user_matrix, indexed_usernames

def get_followers(username):
    # CODE DUPLICATED FROM extract.py NEEDS REFACTORING!!!!
    log_name = "%s%s.json"%(LOG_PATH,username) 
    if os.path.isfile(log_name):
        log = json.loads(open(log_name,'r').read())
        return log[0]['user']['followers_count']
    
def normalize(dist):
    total = sum(dist)
    return dist / total

def entropy(dist):
    return 0 - sum([p * log(p) for p in normalize(dist)])

def main():

    topic_matrix = parse_topics()
    print(topic_matrix.shape)

    user_matrix, indexed_usernames = parse_tweets()
    print(user_matrix.shape)

    x_matrix = dot(user_matrix,topic_matrix)
    print(x_matrix.shape)

    entropies = [entropy(x_matrix[i,:]) for i in range(x_matrix.shape[0])]

    print(entropies)

    # the histogram of the data
    n, bins, patches = pyplot.hist(entropies, 50)
    print(n)
    pyplot.title("Entropy Histogram")
    pyplot.savefig("entropy_histogram.png", format='png')

    followers = array([get_followers(username) for username in indexed_usernames])
    print(followers)
    n, bins, patches = pyplot.hist(followers,50)
    pyplot.title("Followers Histogram")
    pyplot.savefig("followers_histogram.png", format='png')

    axes(yscale='log')
    #should make the axis scale change with the _variance_ of data
    axis([min(entropies)*0.99, max(entropies)*1.01, min(followers)*0.9, max(followers)*1.1])
    pyplot.plot(entropies,followers,'bo')
    pyplot.title('Entropy vs. Followers')
    pyplot.savefig("ef_plot.png", format='png')

if __name__ == "__main__":
    main()
