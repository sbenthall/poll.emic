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


SORTED_ENTROPY_TOPIC_PATH = "topic-entropy-sorted.txt"

user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
user_topic_matrix = numpy.load('user_topic_matrix.npy')

user_entropies = entropy(user_topic_matrix)

weights,residue,rank,singulars = numpy.linalg.lstsq(normalize(user_topic_matrix),user_entropies)

# the histogram of the data
n, bins, patches = plt.hist(weights, 50)
print(n)
plt.title("Entropy Weights Histogram")
plt.savefig("entropy_weights_histogram.png", format='png')
plt.clf()

topic_usage = sum(normalize(user_topic_matrix))
axes(xscale='log',yscale='log')
plt.plot(weights,topic_usage,'ro')
plt.title('Entropy Weight vs. Usage')
plt.savefig("entropy_usage_plot.png", format='png')






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
sorted_entropy = sorted(enumerate(weights), key=itemgetter(1))

sorted_entropy_topics = open(SORTED_ENTROPY_TOPIC_PATH, 'w')

for index, topic in enumerate(sorted_entropy):
    print index, '\t', topic[0], '\t', topic_dict.get(str(topic[0]))
    sorted_entropy_topics.write("%d\t%d\t%s\n" % (index, topic[0], topic_dict.get(str(topic[0]))))
