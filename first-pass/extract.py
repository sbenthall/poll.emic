import re
import os
import sys
from pprint import pprint as pp

TWEET_PATTERN = "(\w*) (\d*)\nDate\: (.*)\n\n    (.*)\n"
DUMP_PATH = "../sample-data/"
URL_REGEX = "http\://\S*"

def get_log(username):
    log_name = username + ".txt"    
    log = open(log_name,'r')
    return log    

def clean_out_urls(tweet):
    return re.sub(URL_REGEX, '', tweet)

def main():
    if len(sys.argv) > 1 :
        username = sys.argv[1]
    else:
        print("Please provide a username")
        return

    log = get_log(username)
    matches = re.findall(TWEET_PATTERN, log.read())

    try:
        os.mkdir(DUMP_PATH + username)
    except OSError:
        pass # directory already exists

    for (name,number,date,tweet) in matches:
        tweet_file = open("%s/%s/%s-%s.txt" % (DUMP_PATH,username,name,number),'w')

        # clean out URLs to get rid of bogus 'words'
        clean_tweet = clean_out_urls(tweet)

        print(clean_tweet)

        tweet_file.write(clean_tweet)
        tweet_file.close


if __name__ == "__main__":
    main()
