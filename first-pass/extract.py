import re
import os
import sys
from pprint import pprint as pp

TWEET_PATTERN = "(\w*) (\d*)\nDate\: (.*)\n\n    (.*)\n"
LOG_PATH = "log/"
DUMP_PATH = "sample-data/tweets.txt"
URL_REGEX = "http\://\S*"

usernames = ["BarackObama", "SarahPalinUSA"]

def get_log(username):
    log_name = username + ".txt"    
    log = open(LOG_PATH + log_name,'r')
    return log    

def clean_out_urls(tweet):
    return re.sub(URL_REGEX, '', tweet)

def main():

    tweet_file = open("%s" % (DUMP_PATH),'w')

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
