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
from operator import itemgetter

TOPIC_PATH = 'topic-keys.txt'
TOPIC_PATTERN = "(\d*)\s*(0[.]\d*)\s(.*)\n"
SORTED_SPECIALIST_TOPIC_PATH = 'sorted_specialist_topic.txt'
SORTED_GENERALIST_TOPIC_PATH = 'sorted_generalist_topic.txt'

# return an array of "how many topics each user talk about"
def num_of_topic(user_topic_matrix):
    avg = numpy.average(user_topic_matrix)
    print avg
    topic_num_matrix = (user_topic_matrix >avg)
    topic_num_array = sum(topic_num_matrix.T)
    return topic_num_array

def percent_of_topic(user_topic_matrix):
    user_topic_matrix = normalize(user_topic_matrix)
    avg = numpy.average(user_topic_matrix)
    print avg #should be 1/num of topic
    print user_topic_matrix.shape[0]
    topic_pct_matrix = zeros((user_topic_matrix.shape[0],3))
    for user in range(user_topic_matrix.shape[0]):
        for topic in user_topic_matrix[user,:]:
            #print topic
            if topic > avg:
                topic_pct_matrix[user,0] +=1
            else:
                topic_pct_matrix[user,1] +=1
    
    print topic_pct_matrix
    return topic_pct_matrix

#for each topic, how many users talked about them
def topic_usage():
    SORTED_USAGE_TOPIC_PATH = "topic-usage-sorted.txt"
    
    user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
    user_topic_matrix = numpy.load('user_topic_matrix.npy')
    
    topic_usage = sum(normalize(user_topic_matrix))
    
    # the histogram of the data
    n, bins, patches = plt.hist(topic_usage, 50)
    print(n)
    plt.title("Topic Usage Histogram")
    plt.savefig("topic_usage_histogram.png", format='png')
    
    TOPIC_PATH = 'topic-keys.txt'
    
    TOPIC_PATTERN = "(\d*)\s*(0[.]\d*)\s(.*)\n"
    
    #import topics file to dict
    topics = open(TOPIC_PATH)
    topic_dict = dict()
    
    for line in topics.readlines():
        #print line
        topic = re.findall(TOPIC_PATTERN, line)
        for index, value, terms in topic:
            topic_dict[index] = terms
    
    #write sorted use
    sorted_usage = sorted(enumerate(topic_usage), key=itemgetter(1))
    
    sorted_usage_file = open(SORTED_USAGE_TOPIC_PATH, 'w')
    
    for index, topic in enumerate(sorted_usage):
        #print index, '\t', topic[0], '\t', topic_dict.get(str(topic[0]))
        sorted_usage_file.write("%d\t%d\t%s\n" % (index, topic[0], topic_dict.get(str(topic[0]))))
    


topics = open(TOPIC_PATH)
topic_dict = dict()

for line in topics.readlines():
    #print line
    topic = re.findall(TOPIC_PATTERN, line)
    for index, value, terms in topic:
        topic_dict[index] = terms


user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
user_topic_matrix = numpy.load('user_topic_matrix.npy')    
topic_num_array = num_of_topic(user_topic_matrix)

#===========================
#generate diagram topic coverage vs. F&F
#===========================
plt.clf()
n, bins, patches = plt.hist(topic_num_array, 50)
plt.title("num of topic Histogram")
plt.savefig("num_of_topic_histogram.png", format='png')
    
plt.clf()
axes(yscale='log')
plt.plot(topic_num_array, user_metadata_matrix[:,0], 'bo')
plt.title('num of topic vs. follower')
plt.savefig("num of topic vs. follower.png", format='png')

plt.clf()
axes(yscale='log')
plt.plot(topic_num_array, user_metadata_matrix[:,1], 'bo')
plt.title('num of topic vs friend')
plt.savefig("num of topic vs friend.png", format='png')



topic_pct_matrix = percent_of_topic(user_topic_matrix)

plt.clf()
axes(yscale='log')
plt.plot(topic_pct_matrix[:,0], user_metadata_matrix[:,0], 'bo')
plt.title('percent of topic vs. follower')
plt.savefig("percent of topic vs. follower.png", format='png')


total_topic = user_topic_matrix.sum(axis=1)

plt.clf()
axes(yscale='log', xscale='log')
plt.plot(total_topic, user_metadata_matrix[:,0], 'bo')
plt.title('total topic vs. follower')
plt.savefig("total topic vs. follower.png", format='png')


#===========================
#write sorted special topics
#===========================
specialist = (numpy.nonzero(topic_num_array < 10))[0]
#topics that specialists talk about and their hits
specialist_topic_array = sum(user_topic_matrix[specialist,:] > numpy.average(user_topic_matrix))
sorted_specialist_topics = sorted(enumerate(specialist_topic_array), key=itemgetter(1), reverse=True)
    
sorted_specialist_topics_file = open(SORTED_SPECIALIST_TOPIC_PATH, 'w')

for rank, (index, hit) in enumerate(sorted_specialist_topics):
    if rank < 20:
        print rank, index, hit, topic_dict.get(str(index))
    sorted_specialist_topics_file.write("%d\t%d\t%d\t%s\n" % (rank, index, hit, topic_dict.get(str(index))))


#===========================
#write sorted general topics
#===========================
generalist = (numpy.nonzero(topic_num_array > 100))[0]
#topics that generalists talk about and their hits
generalist_topic_array = sum(user_topic_matrix[generalist,:] > numpy.average(user_topic_matrix))
sorted_generalist_topics = sorted(enumerate(generalist_topic_array), key=itemgetter(1), reverse=True)
    
sorted_generalist_topics_file = open(SORTED_GENERALIST_TOPIC_PATH, 'w')

for rank, (index, hit) in enumerate(sorted_generalist_topics):
    if rank < 20:
        print rank, index, hit, topic_dict.get(str(index))
    sorted_generalist_topics_file.write("%d\t%d\t%d\t%s\n" % (rank, index, hit, topic_dict.get(str(index))))


    