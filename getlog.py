import os
import sys
import simplejson as json
from pprint import pprint as pp
from authtwitter import twitter
from twitter import TwitterHTTPError
import time
from settings import *
from utils import *

if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

def use_statuses_api(screen_name):
    log_path = "%s%s.json" % (LOG_PATH, screen_name)

    if os.path.isfile(log_path):
        print "File %s already exists, not overwriting" % (log_path)
        return

    #helper method needed for exponential dropoff
    def call_api(screen_name, sleep_exp):
        try:
            tweets = twitter.statuses.user_timeline(screen_name=screen_name,count=200,include_rts=1)
            pp("Collected tweets for "+ screen_name)
            file = open(log_path, 'w')
            file.write(json.dumps(tweets))
            time.sleep(SLEEP)
        except TwitterHTTPError as e:
            if e.e.code == 502:
                #if breaks due to twitter overload error,
                #back off exponentially
                #as per twitter doc recommendation
                print("Error 502 for %s. Will sleep with factor %d" % (screen_name,sleep_exp))
                time.sleep(SLEEP ** sleep_exp)
                sleep_exp += 1
                call_api(screen_name,sleep_exp)
            else:
                print(e) 
                time.sleep(SLEEP)

    sleep_exp = 1
    call_api(screen_name,sleep_exp)
        



snowball = load_snowball()

for u_id, metadata in snowball.items():
    #print "crawling: ", line
    if metadata.has_key('screen_name'):
        screen_name = metadata['screen_name']
        
        use_statuses_api(screen_name)
    else:
        print 'No screen name for %s'%(u_id)



