import re
from settings import *
from utils import *
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
from math import log
import matplotlib.pyplot as pyplot
import os
import simplejson as json
from pylab import axes, axis

user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
user_topic_matrix = numpy.load('user_topic_matrix.npy')

def main():

    entropies = entropy(user_topic_matrix)

    followers = user_metadata_matrix[:,1]
    print(followers)
    n, bins, patches = pyplot.hist(followers,50)
    pyplot.title("Friends Histogram")
    pyplot.savefig("friends_histogram.png", format='png')

    axes(yscale='log')
    #should make the axis scale change with the _variance_ of data
    axis([min(entropies), max(entropies), 0, max(followers)*1.1])
    pyplot.plot(entropies,followers,'bo')
    pyplot.title('Entropy vs. Friends')
    pyplot.savefig("entropy_friends_plot.png", format='png')

if __name__ == "__main__":
    main()
