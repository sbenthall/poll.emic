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


#write sorted entropy
sorted_usage = sorted(enumerate(topic_usage), key=itemgetter(1))

sorted_usage_file = open(SORTED_USAGE_TOPIC_PATH, 'w')

for index, topic in enumerate(sorted_usage):
    print index, '\t', topic[0], '\t', topic_dict.get(str(topic[0]))
    sorted_usage_file.write("%d\t%d\t%s\n" % (index, topic[0], topic_dict.get(str(topic[0]))))
