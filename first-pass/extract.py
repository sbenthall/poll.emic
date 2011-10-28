import re
import os
import sys
from pprint import pprint as pp
import simplejson as json

LOG_PATH = "log/"
DUMP_PATH = "sample-data/"
DUMP_FILE = "sample-data/tweets.txt"

JSON_LOG = True

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

def get_screen_names():
    snowball = load_snowball()
    pp(snowball)
    return [m['screen_name'] for m in snowball.values() if m.has_key('screen_name')]


URL_REGEX = "http\://\S*"
def clean(tweet):
    clean_tweet = re.sub(URL_REGEX, '', tweet)
    clean_tweet = re.sub("[\n\r\t]",' ',clean_tweet)
    #clean out retweet 'RT'
    clean_tweet = re.sub("^RT ",'',clean_tweet)
    return clean_tweet


def get_txt_log(username):    
    log_path = "%s%s.txt"%(LOG_PATH,username) 
    if os.path.isfile(log_name):
        log = open(log_name,'r')
        return log.read()    
    else:
        print "No log %s found, returning blank" % (log_name)
        return ""

TWEET_PATTERN = "(\w*) (\d*)\nDate\: (.*)\n\n    (.*)\n"
def parse_txt_log(username):    
    log = get_txt_log(username)
    matches = re.findall(TWEET_PATTERN, log)

    return [clean(tweet) for (name,number,date,tweet) in matches]

def parse_json_log(username):
    log_name = "%s%s.json"%(LOG_PATH,username) 
    if os.path.isfile(log_name):
        log = json.loads(open(log_name,'r').read())
        return [clean(tweet['text']) for tweet in log]
    else:
        print "No log %s found, returning blank" % (log_name)
        return ""

def main():
    if not os.path.exists(DUMP_PATH):
	    os.makedirs(DUMP_PATH)

    # w+ create file if it doesn't exist, but overwrite if it does    
    tweet_file = open("%s" % (DUMP_FILE),'w+')

    screen_names = get_screen_names()
    
    for screen_name in screen_names:

        clean_tweets = []
        if JSON_LOG:
            clean_tweets = parse_json_log(screen_name)
        else:
            clean_tweets = parse_txt_log(screen_name)

        if len(clean_tweets) < 200:
            print "%s has fewer than 200 tweets.  Leaving out of sample data."%(screen_name)
        else:
            for clean_tweet in clean_tweets:
                print(clean_tweet)
                try:
                    tweet_file.write(u"twitter %s %s\n" % (screen_name, clean_tweet))

                    tweet_file.flush()
                except:
                    'Error: Exception writing this tweet'

    tweet_file.close()

if __name__ == "__main__":
    main()
