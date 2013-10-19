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

if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

logger = logging.getLogger('getsnowball')
#todo: use date/time as the log file name
hdlr = logging.FileHandler('./logging/getsnowball.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)


CACHE_LOOKUP_PATH = os.path.join(CACHE_PATH,"twitter.users.lookup")
if not os.path.exists(CACHE_LOOKUP_PATH):
    os.makedirs(CACHE_LOOKUP_PATH)

CACHE_FRIENDS_PATH = os.path.join(CACHE_PATH,"twitter.friends.ids")
if not os.path.exists(CACHE_FRIENDS_PATH):
    os.makedirs(CACHE_FRIENDS_PATH)

CACHE_FOLLOWERS_PATH = os.path.join(CACHE_PATH,"twitter.followers.ids")
if not os.path.exists(CACHE_FOLLOWERS_PATH):
    os.makedirs(CACHE_FOLLOWERS_PATH)


def lookup(user_id):
    # return user's metadata information
    file_path = os.path.join(CACHE_LOOKUP_PATH,"%s.json" % user_id)
    if os.path.isfile(file_path):
        logger.debug("id: %s exists in cache." % user_id)
        file = open(file_path)
        return json.loads(file.read())
    else:
        logger.debug("id: %s does not exists in cache. Will retrieve it from web." % user_id)
        try:
            metadata = call_api(twitter.users.lookup,
                                {'user_id':user_id})[0]
            file = open(file_path, 'w')
            file.write(json.dumps(metadata))
            return metadata
        except TwitterHTTPError as e:
            print e
            logger.error(e)
            #hack to prevent crawling this
            return {'followers_count': 0, 'error': e}

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
                    file_path = os.path.join(CACHE_LOOKUP_PATH,"%s.json" % user['id'])
                    file = open(file_path,'w')
                    file.write(json.dumps(user))

            except TwitterHTTPError as e:
                print e
                logger.error(e)


API_URL = "http://api.twitter.com/1/"

def get_friends(user_id):
    file_path = os.path.join(CACHE_FRIENDS_PATH,"%s.json" % user_id)
    if os.path.isfile(file_path):
        logger.debug("friends id: %s exists in cache." % user_id)
        file = open(file_path)
        return set(json.loads(file.read()))
    else:
        try:
            #watch out, new API change includes cursor info
            #by default
            friends_response = call_api(twitter.friends.ids,
                                        {'user_id':user_id})
            friends = friends_response['ids']
            print(friends_response)
            logger.debug("id: %s \n friends: %s ", user_id, friends)
            file = open(file_path, 'w')
            file.write(json.dumps(friends))
            return set(friends)
        except TwitterHTTPError as e:
            print e
            return set()

def get_followers(user_id):
    file_path = os.path.join(CACHE_FOLLOWERS_PATH,"%s.json" % user_id)
    if os.path.isfile(file_path):
        logger.debug("follower id: %s exists in cache." % user_id)
        file = open(file_path)
        return set(json.loads(file.read()))
    else:
        try:
            followers_response = call_api(twitter.followers.ids,
                                          {'user_id':user_id})
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

def use_statuses_api(screen_name):
    log_path = "%s%s.json" % (LOG_PATH, screen_name)

    if os.path.isfile(log_path):
        print "File %s already exists, not overwriting" % (log_path)
        return

    try:
        tweets = call_api(twitter.statuses.user_timeline,
                          {'screen_name': screen_name,
                           'count': 200,
                           'include_rts': 1
                           })
        pp("Collected tweets for "+ screen_name)
        file = open(log_path, 'w')
        file.write(json.dumps(tweets))
    except TwitterHTTPError as e:
        print("Exception raised for %s.  Continuing." % (screen_name))
        time.sleep(SLEEP)
