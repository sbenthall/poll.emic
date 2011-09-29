import re
import os
import sys
from pprint import pprint as pp

NAME_PATH = "names.txt"
TWEET_PATTERN = "(\w*) (\d*)\nDate\: (.*)\n\n    (.*)\n"
LOG_PATH = "log/"
DUMP_PATH = "sample-data/"
DUMP_FILE = "sample-data/tweets.txt"
URL_REGEX = "http\://\S*"

usernames = []

def get_name():

    if os.path.isfile("%s" % (NAME_PATH)):
        names = open("%s" % (NAME_PATH),'r')
        return names
    else:
        print "error"
        return ""
        
def get_log(username):
    
    log_name = username + ".txt"    
    log = open(LOG_PATH + log_name,'r')
    return log    

def clean_out_urls(tweet):
    return re.sub(URL_REGEX, '', tweet)

def main():
    if not os.path.exists(DUMP_PATH):
	    os.makedirs(DUMP_PATH)

    # w+ create file if it doesn't exist, but overwrite if it does    
    tweet_file = open("%s" % (DUMP_FILE),'w+')

    names = get_name()
    for line in names:
        usernames.append(line.strip())
    print usernames
    
    for username in usernames:
        
        log = get_log(username)
        matches = re.findall(TWEET_PATTERN, log.read())

        for (name,number,date,tweet) in matches:
            # clean out URLs to get rid of bogus 'words'
            clean_tweet = clean_out_urls(tweet)

            print(clean_tweet)

            tweet_file.write("twitter %s %s\n" % (username, clean_tweet))
            tweet_file.flush()

    tweet_file.close()

if __name__ == "__main__":
    main()
