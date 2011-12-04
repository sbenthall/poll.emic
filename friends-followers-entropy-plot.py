import re
from settings import *
from utils import get_followers_count
from pprint import pprint as pp
import numpy
from numpy import array,zeros,ones,dot
from math import log
import matplotlib.pyplot as plt
import os
import simplejson as json
from pylab import axes, axis
from mpl_toolkits.mplot3d import Axes3D

user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
user_topic_matrix = numpy.load('user_topic_matrix.npy')
    
def normalize(dist):
    total = sum(dist)
    return dist / total

def entropy(dist):
    return 0 - sum([p * log(p) for p in normalize(dist)])


def main():

    followers = user_metadata_matrix[:,0]
    friends = user_metadata_matrix[:,1]
    entropies = [entropy(user_topic_matrix[i,:]) for i in range(user_topic_matrix.shape[0])]

    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(friends,followers,entropies)

    ax.set_xlabel('Followers')
    ax.set_ylabel('Friends')
    ax.set_zlabel('Entropy')

    plt.title('Followers vs. Friends vs. Entropy')
    plt.savefig("followers_friends_plot.png", format='png')

if __name__ == "__main__":
    main()
