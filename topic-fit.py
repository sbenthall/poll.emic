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

weights = numpy.linalg.lstsq(user_topic_matrix,numpy.log10(user_metadata_matrix + 1))

print weights
