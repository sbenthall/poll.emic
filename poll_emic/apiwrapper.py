from twitter import Twitter, TwitterHTTPError
import ConfigParser
import urllib2
import simplejson as json
import logging
import os
import random
from authtwitter import twitter
from utils import *
import sys
from pprint import pprint as pp
import time
from utils import *
import ConfigParser


config= ConfigParser.ConfigParser()
config.read('config.cfg')

CACHE_PATH = config.get('Settings','cachepath')

# better to integrate with the method declarations.
method_names = ["twitter.users.lookup",
                "twitter.friends.ids",
                "twitter.followers.ids"]

for method_name in method_names:
    path = os.path.join(CACHE_PATH,method_name)
    if not os.path.exists(path):
        os.makedirs(path)


if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

logger = logging.getLogger('getsnowball')
#todo: use date/time as the log file name
hdlr = logging.FileHandler('./logging/getsnowball.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

# determine if the UID is a user ID number or a screenname,
# and return the appropriate query parameter name
def id_or_sn(uid):
    if isinstance(uid,int):
        return 'user_id'
    elif isinstance(uid,str):
        return 'screen_name'
    else:
        raise Exception("UID %s is neither integer nor string" % uid)

def call_api_with_cache(user_id, method, method_name):
    # first check the cache
    file_path = os.path.join(CACHE_PATH,method_name,"%s.json" % user_id)
    if os.path.isfile(file_path):
        logger.debug("%s %s exists in cache." % (method_name, user_id))
        file = open(file_path)
        return json.loads(file.read())
    else:
    # if not in cache call the API
        logger.debug("%s %s does not exists in cache. Will retrieve it from web." % (method_name, user_id))
        try:
            data = call_api(method,
                            {id_or_sn(user_id):user_id})
            file = open(file_path, 'w')
            file.write(json.dumps(data))
            return data
        except TwitterHTTPError as e:
            print e
            logger.error(e)
            #hack to prevent crawling this
            return {'error': e}

def lookup(user_id):
    return call_api_with_cache(user_id,
                               twitter.users.lookup,
                               'twitter.users.lookup')

def get_friends(user_id):
    data =  call_api_with_cache(user_id,
                                twitter.friends.ids,
                                'twitter.friends.ids')

    friends = set(data['ids'])

    return friends



def lookupMulti(user_ids):
    """ """
    if len(user_ids) > 100:
        print("Attempting lookup on %d, paring down." % len(user_ids))
        s = set()
        while len(user_ids) > 0:
            if len(s) == 100:
                print("Looking up subset, %d to go" % len(user_ids))
                lookupMulti(s)
                s = set()
            s.add(user_ids.pop())
    else:
        new_ids = set()
        for id in user_ids:
            file_path = os.path.join(CACHE_LOOKUP_PATH,"%s.json" % id)
            if not os.path.isfile(file_path):
                new_ids.add(id)
    
        print "new ID: ", new_ids
        logger.debug("new ID: %s", new_ids)
    
        if len(new_ids) > 0:
            query = ",".join([str(x) for x in new_ids])
            logger.debug(query)
            try:
                metadatas = call_api(twitter.users.lookup,
                                     {'user_id':query})
                for user in metadatas:
                    logger.debug(user)
                    file_path = os.path.join(CACHE_PATH,"twitter.users.lookup","%s.json" % user['id'])
                    file = open(file_path,'w')
                    file.write(json.dumps(user))

            except TwitterHTTPError as e:
                print e
                logger.error(e)

def get_followers(user_id):
    file_path = os.path.join(CACHE_FOLLOWERS_PATH,"%s.json" % user_id)
    if os.path.isfile(file_path):
        logger.debug("follower id: %s exists in cache." % user_id)
        file = open(file_path)
        return set(json.loads(file.read()))
    else:
        try:
            followers_response = call_api(twitter.followers.ids,
                                          {id_or_sn(user_id):user_id})
            logger.debug("id: %s \n followers response: %s "% (user_id, followers_response))
            followers = followers_response['ids']
            logger.debug("id: %s \n followers: %s ", user_id, followers)
            file = open(file_path, 'w')
            file.write(json.dumps(followers))
            return set(followers)
        except TwitterHTTPError as e:
            print e
            return set()


if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

CACHE_STATUSES_PATH = os.path.join(CACHE_PATH,"twitter.statuses.user_timeline")
if not os.path.exists(CACHE_STATUSES_PATH):
    os.makedirs(CACHE_STATUSES_PATH)

# shouldn't be hard coded here...
SLEEP = 5

def use_statuses_api(screen_name):
    log_path = os.path.join(CACHE_STATUSES_PATH,"%s.json" % screen_name)

    if os.path.isfile(log_path):
        logger.debug("statuses for username: %s exists in cache." % screen_name)
        file = open(log_path)
        return json.loads(file.read())
    try:
        tweets = call_api(twitter.statuses.user_timeline,
                          {id_or_sn(screen_name): screen_name,
                           'count': 200,
                           'include_rts': 1
                           })
        pp("Collected tweets for "+ screen_name)
        file = open(log_path, 'w')
        file.write(json.dumps(tweets))
        return tweets
    except TwitterHTTPError as e:
        print("Exception raised for %s.  Continuing." % (screen_name))
        time.sleep(SLEEP)
