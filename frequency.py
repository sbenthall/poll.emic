import re
import os
import sys
from pprint import pprint as pp
import simplejson as json
from settings import *
from utils import *
import datetime
import numpy
from numpy import array,zeros,ones,dot
import preparedata
from math import log
import matplotlib.pyplot as plt
from pylab import axes, axis

month_dict = {"Jan":1,"Feb":2,"Mar":3,"Apr":4, "May":5, "Jun":6,
              "Jul":7,"Aug":8,"Sep":9,"Oct":10,"Nov":11,"Dec":12}

TIME_REG = "\w*\s(\w*)\s(\d*)\s(\d*)[:](\d*)[:]\d*\s\S*\s(\w*)"
USER_INDEX_PATH = "indexed_usernames.json"
USER_FREQ_PATH = "user_freq.json"

def calculate_frequency(username):
    log_name = "%s%s.json"%(LOG_PATH,username)
    time_stamps = list() 
    if os.path.isfile(log_name):
        log = json.loads(open(log_name,'r').read())
        time1 = None
        for tweet in log:
            time = re.findall(TIME_REG, tweet['created_at'])
            #print tweet['created_at']
            for month, day, hour, minute, year in time:
                #print year, month, day, hour, ':',  minute
                #print type(month_dict[month]), type(day), type(hour), type(minute)
                time2 = datetime.datetime(int(year), month_dict[month], 
                                          int(day), int(hour), int(minute))
                #print time2
                if time1 != None:
                    time_diff = time1 - time2
                    #print time_diff
                    #print time_diff.total_seconds()/3600
                    time_stamps.append(time_diff.total_seconds()/3600)
                time1 = time2    
                
        #return [clean(tweet['text']) for tweet in log]
        return time_stamps
    else:
        print "No log %s found, returning blank" % (log_name)
        return ""

def get_user_index():
    user_tweet_matrix, indexed_usernames = preparedata.parse_tweets()
    file = open(USER_INDEX_PATH, 'w')
    file.write(json.dumps(indexed_usernames))
    file.close()

def calculate_all_freq():
    indexed_usernames = json.loads(open(USER_INDEX_PATH,'r').read())
    freq = list()
    std = list()
    
    for screen_name in indexed_usernames:
        time_stamp = calculate_frequency(screen_name)
        #print time_stamp
        #print (1/numpy.average(time_stamp))*24    #tweets per day
        freq.append((1/numpy.average(time_stamp))*24)   #duration per tweet (hr)
        std.append(numpy.std(time_stamp))
        #print numpy.average(time_stamp)
        #print numpy.std(time_stamp)
        
    file = open(USER_FREQ_PATH, 'w')
    file.write(json.dumps([freq, std]))
    file.close()    

def generate_user_freq_matrix():
    user_metadata_matrix = numpy.load('user_metadata_matrix.npy')
    freq_std = json.loads(open(USER_FREQ_PATH,'r').read())

    user_freq_matrix = zeros((len(user_metadata_matrix),4))
    
    user_freq_matrix[:,0] = user_metadata_matrix[:,0]
    user_freq_matrix[:,1] = user_metadata_matrix[:,1]
    user_freq_matrix[:,2] = freq_std[0]
    user_freq_matrix[:,3] = freq_std[1]
    
    print user_freq_matrix
    numpy.save('user_freq_matrix', user_freq_matrix)
    print "Saved user_tweet_matrix"
        
def main():
    
    #calculate_all_freq()
    #generate_user_freq_matrix()
    
    user_freq_matrix = numpy.load('user_freq_matrix.npy')
    print user_freq_matrix
    indexed_usernames = json.loads(open(USER_INDEX_PATH,'r').read())
    for index, freq in enumerate(user_freq_matrix[:,2]):
        if freq > 100:
            print indexed_usernames[index], freq
            
    axes(yscale='log')
    axis([0, 20, 1, max(user_freq_matrix[:,0])])
    plt.plot(user_freq_matrix[:,2], user_freq_matrix[:,0], 'bo')
    plt.title('frequency vs. follower')
    plt.savefig("frequency vs. follower.png", format='png')
    
    plt.clf()
    frequency = user_freq_matrix[:,2]
    n, bins, patches = plt.hist(frequency,100)
    plt.title("frequency Histogram")
    plt.savefig("frequency_histogram.png", format='png')
    
    plt.clf()
    axes(yscale='log')
    axis([0, 200, 1, max(user_freq_matrix[:,0])])
    plt.plot(user_freq_matrix[:,3], user_freq_matrix[:,0], 'bo')
    plt.title('consistency vs. follower')
    plt.savefig("consistency vs. follower.png", format='png')    
        
    #numpy.append(user_metadata_matrix, [[freq_list]], axis=1)
    

    
if __name__ == "__main__":
    main()
