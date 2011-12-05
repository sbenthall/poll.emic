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

user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
user_topic_matrix = numpy.load('user_topic_matrix.npy')

normalized_user_topic_matrix = normalize(user_topic_matrix.T).T

weights,residue,rank,singulars = numpy.linalg.lstsq(normalized_user_topic_matrix,numpy.log10(user_metadata_matrix + 1))

plt.plot(weights[:,0],weights[:,1],'bo')
plt.title('Followers Weight vs. Friend Weight')
plt.savefig("n_weights_plot.png", format='png')

print numpy.find(weights[:,0]>50)
