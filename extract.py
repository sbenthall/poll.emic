import re
import os
import sys
from pprint import pprint as pp
import simplejson as json
from settings import *
from utils import *

if len(sys.argv) > 1:
    SNOWBALL_PATH = sys.argv[1]

def get_screen_names():
    snowball = load_snowball()
    return [m['screen_name'] for m in snowball.values() if m.has_key('screen_name')]


URL_REGEX = "http\://\S*"
def clean(tweet):
    clean_tweet = re.sub(URL_REGEX, '', tweet)
    clean_tweet = re.sub("[\n\r\t]",' ',clean_tweet)
    #clean out retweet 'RT'
    clean_tweet = re.sub("^RT ",'',clean_tweet)

    if AGGREGATE_TWEETS:
        try:
            clean_tweet.decode('ascii')
        except UnicodeEncodeError:
            return ""

    return clean_tweet

def parse_json_log(username):
    log_name = "%s%s.json"%(LOG_PATH,username) 
    if os.path.isfile(log_name):
        log = json.loads(open(log_name,'r').read())
        return [clean(tweet['text']) for tweet in log]
    else:
        print "No log %s found, returning blank" % (log_name)
        return ""


if not os.path.exists(DUMP_PATH):
    os.makedirs(DUMP_PATH)


def main():
    # w+ create file if it doesn't exist, but overwrite if it does    
    tweet_file = open("%s" % (DUMP_FILE),'w+')

    screen_names = get_screen_names()
    
    for screen_name in screen_names:

        print("Parsing tweets for %s" % screen_name)
        clean_tweets = []
        clean_tweets = parse_json_log(screen_name)

        if len(clean_tweets) < CUTOFF:
            print "%s has fewer than %d tweets.  Leaving out of sample data."%(screen_name, CUTOFF)
        else:
            if not AGGREGATE_TWEETS:
                for clean_tweet in clean_tweets:
                    print(clean_tweet)
                    try:
                        tweet_file.write(u"twitter %s %s\n" % (screen_name, clean_tweet))

                        tweet_file.flush()
                    except:
                        'Error: Exception writing this tweet'
            else:
                all_tweets = " ".join(clean_tweets)
                print(all_tweets)
                tweet_file.write(u"twitter %s %s\n" % (screen_name, all_tweets))

                tweet_file.flush()



    tweet_file.close()

if __name__ == "__main__":
    main()
