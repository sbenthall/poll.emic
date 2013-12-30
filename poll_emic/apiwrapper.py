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
                "twitter.followers.ids",
                "twitter.statuses.user_timeline"]

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
def id_or_sn(query):
    if isinstance(query,int):
        return 'user_id'
    elif isinstance(query,str):
        return 'screen_name'
    elif isinstance(query,list) and len(query) > 0:
        if isinstance(query[0],int):
            return 'user_id'
        elif isinstnace(query[0],str):
            return 'screen_name'
    else:
        raise Exception("UID %s is a %s, not an integer nor string nor a nonempty list" % (query,str(type(query))))

def cache_file_path(method_name,user):
    return os.path.join(CACHE_PATH,method_name,"%s.json" % user)

def is_cached(method_name,user):
    return os.path.isfile(cache_file_path(method_name,user))

def cache(method_name,user,data):
    cache_file = open(cache_file_path(method_name,user), 'w')
    cache_file.write(json.dumps(data))

def call_api_with_cache(user_id, method, method_name):
    # first check the cache
    if is_cached(method_name,user_id):
        logger.debug("%s %s exists in cache." % (method_name, user_id))
        file = open(cache_file_path(method_name,user_id))
        return json.loads(file.read())
    else:
    # if not in cache call the API
        logger.debug("%s %s does not exists in cache. Will retrieve it from web." % (method_name, user_id))
        try:
            data = call_api(method,
                            {id_or_sn(user_id):user_id})
            cache(method_name,user_id,data)
            return data
        except TwitterHTTPError as e:
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
    method_name = 'twitter.users.lookup'
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
        new_ids = [user for user in user_ids if not is_cached(method_name,user)]

        print "new ID: ", new_ids
        logger.debug("new ID: %s", new_ids)
    
        if len(new_ids) > 0:
            query = ",".join([str(x) for x in new_ids])
            logger.debug(query)
            try:
                metadatas = call_api(twitter.users.lookup,
                                     {id_or_sn(query):query})
                for user_data in metadatas:
                    cache(method_name,user_data['screen_name'],user_data)

                return metadatas

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

def use_statuses_api(screen_name):
    method_name = "twitter.statuses.user_timeline"
    log_path = cache_file_path(method_name,screen_name)

    if is_cached(method_name,screen_name):
        logger.debug("statuses for username: %s exists in cache." % screen_name)
        file = open(log_path)
        return json.loads(file.read())
    try:
        tweets = call_api(twitter.statuses.user_timeline,
                          {id_or_sn(screen_name): screen_name,
                           'count': 200,
                           'include_rts': 1
                           })

        file = open(log_path, 'w')
        file.write(json.dumps(tweets))
        return tweets
    except TwitterHTTPError as e:
        print("Exception raised for %s.  Continuing." % (screen_name))
        return []
