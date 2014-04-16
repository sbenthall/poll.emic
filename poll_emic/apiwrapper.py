from twitter import Twitter, TwitterHTTPError
import cache
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

LOGGING_PATH = config.get('Settings','loggingpath')

if not os.path.exists(LOGGING_PATH):
    os.makedirs(LOGGING_PATH)

##cruft?
logger = logging.getLogger('getsnowball')
#todo: use date/time as the log file name
hdlr = logging.FileHandler('./' + LOGGING_PATH + '/mentionball.log')
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


def call_api_with_cache(user_id, method, method_name,parameters={}):
    # first check the cache
    if cache.has(method_name,user_id):
        logger.debug("%s %s exists in cache." % (method_name, user_id))
        return cache.read(method_name,user_id)
    else:
    # if not in cache call the API
        logger.debug("%s %s does not exists in cache. Will retrieve it from web." % (method_name, user_id))
        try:
            data = call_api(method,
                            dict([(id_or_sn(user_id),user_id)]
                            + parameters.items()))
            cache.write(method_name,user_id,data)
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

    new_users = []
    cached_users = []

    for user in user_ids:
        if cache.has(method_name,user):
            cached_users.append(user)
        else:
            new_users.append(user)

    data = {}

    for user in cached_users:
        data[user] = lookup(user)
        if type(lookup(user)) is list:
            pp('Watch out for %s' % user)

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
                cache.write(method_name,screen_name,user_data)
                data[screen_name] = user_data

        except TwitterHTTPError as e:
            print e
            logger.error(e)

    return data

def get_members_from_list(owner,slug):

    cursor = -1
    users = []
 
    pp("Gettings users from list @%s/%s" % (owner,slug))

    while cursor != 0:
        pp("cursor: %d" % cursor)
        response_dictionary = call_api(twitter.lists.members,
                                       {'owner_screen_name':owner,
                                        'slug':slug,
                                        'cursor':cursor})
        users.extend(response_dictionary['users'])
        cursor = response_dictionary['next_cursor']

    pp('Retrieved %d users from list' % len(users))

    return [user['screen_name'] for user in users]
