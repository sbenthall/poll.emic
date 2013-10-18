from twitter import Twitter, TwitterHTTPError
import ConfigParser
import urllib2
import simplejson as json
import logging
import os
import random
from settings import *
from authtwitter import twitter
from utils import *

if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

logger = logging.getLogger('getsnowball')
#todo: use date/time as the log file name
hdlr = logging.FileHandler('./logging/getsnowball.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)



if not os.path.exists(METADATA_PATH):
    os.makedirs(METADATA_PATH)


if not os.path.exists(FRIENDS_PATH):
    os.makedirs(FRIENDS_PATH)

if not os.path.exists(FOLLOWERS_PATH):
    os.makedirs(FOLLOWERS_PATH)


def lookup(user_id):
    # return user's metadata information
    if os.path.isfile("%s%s.json" % (METADATA_PATH, user_id)):
        logger.debug("id: %s exists in cache." % user_id)
        file = open("%s%s.json" % (METADATA_PATH, user_id))
        return json.loads(file.read())
    else:
        logger.debug("id: %s does not exists in cache. Will retrieve it from web." % user_id)
        try:
            metadata = call_api(twitter.users.lookup,
                                {'user_id':user_id})[0]
            file = open("%s%s.json" % (METADATA_PATH, user_id), 'w')
            file.write(json.dumps(metadata))
            return metadata
        except TwitterHTTPError as e:
            print e
            logger.error(e)
            #hack to prevent crawling this
            return {'followers_count': 0, 'error': e}

API_URL = "http://api.twitter.com/1/"

def get_friends(user_id):
    if os.path.isfile("%s%s.json" % (FRIENDS_PATH, user_id)):
        logger.debug("friends id: %s exists in cache." % user_id)
        file = open("%s%s.json" % (FRIENDS_PATH, user_id))
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
            file = open("%s%s.json" % (FRIENDS_PATH, user_id), 'w')
            file.write(json.dumps(friends))
            return set(friends)
        except TwitterHTTPError as e:
            print e
            return set()

def get_followers(user_id):
    if os.path.isfile("%s%s.json" % (FOLLOWERS_PATH, user_id)):
        logger.debug("follower id: %s exists in cache." % user_id)
        file = open("%s%s.json" % (FOLLOWERS_PATH, user_id))
        return set(json.loads(file.read()))
    else:
        try:
            followers_response = call_api(twitter.followers.ids,
                                          {'user_id':user_id})
            logger.debug("id: %s \n followers response: %s "% (user_id, followers_response))
            followers = followers_response['ids']
            logger.debug("id: %s \n followers: %s ", user_id, followers)
            file = open("%s%s.json" % (FOLLOWERS_PATH, user_id), 'w')
            file.write(json.dumps(followers))
            return set(followers)
        except TwitterHTTPError as e:
            print e
            return set()
