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

##cruft?
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
    elif isinstance(query,unicode):
        return 'screen_name'
    elif isinstance(query,list) and len(query) > 0:
        ## should make this not assume nonhomogenous lists
        ## and handle them gracefully
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

def clear_cache(method_name,users):
    ## TO DO: option to clear whole cache
    users = [users] if type(users) is not list else users

    for user in users:
        if is_cached(method_name,user):
            os.remove(cache_file_path(method_name,user))

def read_cache(method_name,user):
        file = open(cache_file_path(method_name,user))
        return json.loads(file.read())
    

def call_api_with_cache(user_id, method, method_name,parameters={}):
    # first check the cache
    if is_cached(method_name,user_id):
        logger.debug("%s %s exists in cache." % (method_name, user_id))
        return read_cache(method_name,user_id)
    else:
    # if not in cache call the API
        logger.debug("%s %s does not exists in cache. Will retrieve it from web." % (method_name, user_id))
        try:
            data = call_api(method,
                            dict([(id_or_sn(user_id),user_id)]
                            + parameters.items()))
            cache(method_name,user_id,data)
            return data
        except TwitterHTTPError as e:
            logger.error(e)
            #hack to prevent crawling this
            return {'error': e}

def lookup(user_id):
    data = call_api_with_cache(user_id,
                               twitter.users.lookup,
                               'twitter.users.lookup')

    #terrible hack -- why do I need this?
    if isinstance(data,list):
        data = data[0]

    return data

def get_friends(user_id):
    data = call_api_with_cache(user_id,
                               twitter.friends.ids,
                               'twitter.friends.ids')

    friends = set(data['ids'])

    return friends

def get_followers(user_id):
    data = call_api_with_cache(user_id,
                               twitter.followers.ids,
                               'twitter.followers.ids')

    friends = set(data['ids'])

    return friends

def use_statuses_api(user_id):
    return call_api_with_cache(user_id,
                               twitter.statuses.user_timeline,
                               'twitter.statuses.user_timeline',
                               parameters={'count' : 200,
                                           'include_rts':1})

def lookup_many(user_ids):
    """ """
    method_name = 'twitter.users.lookup'

    new_users = [user for user in user_ids
               if not is_cached(method_name,user)]

    cached_users = [user for user in user_ids
               if is_cached(method_name,user)]

    data = {}

    for user in cached_users:
        data[user] = lookup(user)

    for user_slice in [new_users[x:x+100]
                       for x
                       in xrange(0,len(new_users),100)]:

        query = ",".join([str(x) for x in user_slice])
        logger.debug("Query is %s" % query)

        try:
            metadatas = call_api(twitter.users.lookup,
                                 {id_or_sn(query):query})
            for user_data in metadatas:
                screen_name = user_data['screen_name']
                cache(method_name,screen_name,user_data)
                data[screen_name] = user_data

        except TwitterHTTPError as e:
            print e
            logger.error(e)

    return data
