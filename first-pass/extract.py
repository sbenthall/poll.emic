import re
import os
import sys
from pprint import pprint as pp
import simplejson as json

LOG_PATH = "log/"
DUMP_PATH = "sample-data/"
DUMP_FILE = "sample-data/tweets.txt"

SNOWBALL_PATH = "snowball-47545000-3.json"
if len(sys.argv) > 1:
    SNOWBALL_PATH = sys.argv[1]

def load_snowball():
    if os.path.isfile("%s" % (SNOWBALL_PATH)):
        snowball_file = open("%s" % (SNOWBALL_PATH),'r')
        snowball = json.loads(snowball_file.read())
        return snowball
    else:
        print "error"

TWEET_PATTERN = "(\w*) (\d*)\nDate\: (.*)\n\n    (.*)\n"
URL_REGEX = "http\://\S*"

usernames = []

def get_screen_names():
    snowball = load_snowball()
    pp(snowball)
    return [m['screen_name'] for m in snowball.values() if m.has_key('screen_name')]


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

    screen_names = get_screen_names()
    
    for screen_name in screen_names:
        
        log = get_log(screen_name)
        matches = re.findall(TWEET_PATTERN, log)

        for (name,number,date,tweet) in matches:
            # clean out URLs to get rid of bogus 'words'
            clean_tweet = clean_out_urls(tweet)

            print(clean_tweet)

            tweet_file.write("twitter %s %s\n" % (screen_name, clean_tweet))
            tweet_file.flush()

    tweet_file.close()

if __name__ == "__main__":
    main()
