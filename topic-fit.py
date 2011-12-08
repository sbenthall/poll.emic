import re
from settings import *
from utils import *
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
from math import log
import matplotlib.pyplot as plt
import os
import simplejson as json
from pylab import axes, axis
from mpl_toolkits.mplot3d import Axes3D
from operator import itemgetter

TOPIC_PATH = 'topic-keys.txt'
SORTED_FOLLOWER_TOPIC_PATH = 'topic-follower-sorted.txt'
SORTED_FRIEND_TOPIC_PATH = 'topic-friend-sorted.txt'
TOPIC_PATTERN = "(\d*)\s*(0[.]\d*)\s(.*)\n"

user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
user_topic_matrix = numpy.load('user_topic_matrix.npy')

normalized_user_topic_matrix = normalize(user_topic_matrix.T).T

weights,residue,rank,singulars = numpy.linalg.lstsq(normalized_user_topic_matrix,numpy.log10(user_metadata_matrix + 1))


plt.plot(user_metadata_matrix[:,0],user_metadata_matrix[:,1],'bo')
plt.title('Followers vs. Friends')
plt.savefig("followers-friends_plot.png", format='png')
plt.clf()

plt.plot(weights[:,0],weights[:,1],'bo')
plt.title('Followers Weight vs. Friend Weight')
plt.savefig("n_weights_plot.png", format='png')
plt.clf()

n, bins, patches = plt.hist(weights[:,0], 50)
print(n)
plt.title("Followers Weights Histogram")
plt.savefig("followers_weights_histogram.png", format='png')
plt.clf()

n, bins, patches = plt.hist(weights[:,1], 50)
print(n)
plt.title("Friends Weights Histogram")
plt.savefig("friends_weights_histogram.png", format='png')
plt.clf()

 
#import topics file to dict
topics = open(TOPIC_PATH)
topic_dict = dict()

for line in topics.readlines():
    #print line
    topic = re.findall(TOPIC_PATTERN, line)
    for index, value, terms in topic:
        topic_dict[index] = terms

#get sorted follower
sorted_follower = sorted(enumerate(weights[:,0]), key=itemgetter(1))
sorted_follower.reverse()
print sorted_follower[0:24]
follower_least25 = sorted_follower[len(sorted_follower)-24:len(sorted_follower)]
follower_least25.reverse()
print follower_least25
    
#write sorted follower    
sorted_follower_topics = open(SORTED_FOLLOWER_TOPIC_PATH, 'w')

for index, topic in enumerate(sorted_follower):
    print index, '\t', topic[0], '\t', topic_dict.get(str(topic[0]))
    sorted_follower_topics.write("%d\t%d\t%s\n" % (index, topic[0], topic_dict.get(str(topic[0]))))

#get sorted friend
sorted_friend = sorted(enumerate(weights[:,1]), key=itemgetter(1))
sorted_friend.reverse()
print sorted_friend[0:24]
friend_least25 = sorted_friend[len(sorted_friend)-24:len(sorted_friend)]
friend_least25.reverse()
print friend_least25

#write sorted friend   
sorted_friend_topics = open(SORTED_FRIEND_TOPIC_PATH, 'w')

for index, topic in enumerate(sorted_friend):
    print index, '\t', topic[0], '\t', topic_dict.get(str(topic[0]))
    sorted_friend_topics.write("%d\t%d\t%s\n" % (index, topic[0], topic_dict.get(str(topic[0]))))

plt.clf()
axes(yscale='log')
plt.plot(user_topic_matrix[:,152], user_metadata_matrix[:,0], 'ro')
plt.plot(user_topic_matrix[:,25], user_metadata_matrix[:,0], 'bo')
plt.title('topic Weight vs. Follower')
plt.savefig("152&25_weights_v_follower.png", format='png')
