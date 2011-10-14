from twitter import Twitter, TwitterHTTPError, OAuth
import ConfigParser
import urllib2
import simplejson as json
import logging
import os
import random

logger = logging.getLogger('getsnowball')
#todo: use date/time as the log file name
hdlr = logging.FileHandler('./logging/getsnowball.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

THROTTLE = 1000
CONNECTION_NO = 20
METADATA_PATH = "accounts/metadata/"
FRIENDS_PATH = "accounts/friends/"
FOLLOWERS_PATH = "accounts/followers/"
FILTER_RANDOM = False   #when filter followers, true: pick randomly,
                        #false: pick from beginning
config= ConfigParser.ConfigParser()
config.read('config.cfg')

oauth = OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret'))

twitter = Twitter(auth=oauth)

def lookup(user_id):
    # return user's metadata information
    if os.path.isfile("%s%s.json" % (METADATA_PATH, user_id)):
        logger.debug("id: %s exists in cache." % user_id)
        file = open("%s%s.json" % (METADATA_PATH, user_id))
        return json.loads(file.read())
    else:
        logger.debug("id: %s does not exists in cache. Will retrieve it from web." % user_id)
        try:
            metadata = twitter.users.lookup(user_id=user_id)[0]
            file = open("%s%s.json" % (METADATA_PATH, user_id), 'w')
            file.write(json.dumps(metadata))
        except TwitterHTTPError as e:
            print e
            logger.error(e)
            return {'followers_count': THROTTLE+1} #hack to prevent crawling this        

def lookupMulti(user_ids):
    
    new_ids = set()
    for id in user_ids:
        if not os.path.isfile("%s%s.json" % (METADATA_PATH, id)):
            new_ids.add(id)
    
    print "new ID: ", new_ids
    logger.debug("new ID: %s", new_ids)
    
    if len(new_ids) > 0:
        query = ",".join([str(x) for x in new_ids])
        logger.debug(query)
        try:
            metadatas = twitter.users.lookup(user_id=query)
            for user in metadatas:
                logger.debug(user)
                file = open('%s%s.json'%(METADATA_PATH,user['id']),'w')
                file.write(json.dumps(user))
    
        except TwitterHTTPError as e:
            print e
            logger.error(e)   
        

API_URL = "http://api.twitter.com/1/"

def get_friends(user_id):
    if os.path.isfile("%s%s.json" % (FRIENDS_PATH, user_id)):
        logger.debug("friends id: %s exists in cache." % user_id)
        file = open("%s%s.json" % (FRIENDS_PATH, user_id))
        return set(json.loads(file.read()))
    else:
        try:
            friends = twitter.friends.ids(user_id=user_id)
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
            followers = twitter.followers.ids(user_id=user_id)
            logger.debug("id: %s \n followers: %s ", user_id, followers)
            file = open("%s%s.json" % (FOLLOWERS_PATH, user_id), 'w')
            file.write(json.dumps(followers))
            return set(followers)
        except TwitterHTTPError as e:
            print e
            return set()

def filter(users):
    #to return filtered set of friends or followers
    #to limit the total number of accounts
    if len(users) <= CONNECTION_NO:
        return(users)
    else:
        users = list(users)
        filtered_users = set()        
        if FILTER_RANDOM:
            while True:
                if len(filtered_users) > CONNECTION_NO:
                    break
                no = random.randint(0, len(users)-1)
                filtered_users.add(users[no])
            return filtered_users
        else:
            for counter in range(CONNECTION_NO):
                filtered_users.add(users[counter])
            return filtered_users
    
def get_snowball(start, hops, mutual=False):
    snowball = {} # dictionary of (id, metadata) pairs
    to_crawl = set([start]) # set of user ids
    crawled = set()

    for h in range(hops):
        for user_id in to_crawl:
            if user_id not in crawled:
                new_users = get_friends(user_id)
                metadata = lookup(user_id)                
                
                if user not in snowball:
                    snowball[user] = lookup(user)

                if metadata['followers_count'] < THROTTLE:
                    followers = get_followers(user_id)
                
                    if mutual:
                        #take intersection
                        new_users = [user for user in users_to_add if user in followers]
                    else:
                        #make union
                        new_users.extend(followers)

                        for new_user in new_users:
                            to_crawl.add(new_user)
                
                to_crawl.remove(user_id)
                crawled.add(user_id)

                
    return snowball



def get_snowball_s(start, hops, mutual):
    logger.info("*** snowball starts!!!")
    snowball_set = {}
    to_crawl = set({start})
    
    for h in range(hops):
        # get all friends and followers into queue
        print "hop: ", h
        all_related_users = set()
        
        # batch lookup users and cache into file
        lookupMulti(to_crawl)
        
        for user_id in to_crawl:
            #print "user_id: ", user_id
            if user_id not in snowball_set:
                # call lookup would only look at cache since lookupMulti called in advance
                metadata = lookup(user_id)
                snowball_set[user_id] = metadata
                
                if h == hops-1:
                    pass #final hop, skip collecting freinds and followers
                    
                #elif metadata['followers_count'] > THROTTLE:
                #    print "followers exceed ", THROTTLE, ", skipped"
                
                else:
                    #look into each user's f&f
                    #related_users is a set of accounts that connect to user_id
                    if mutual:
                        #take intersection
                        related_users = filter(get_friends(user_id)).intersection( filter(get_followers(user_id)) )
                    else:
                        #make union
                        related_users = filter(get_friends(user_id)).union( filter(get_followers(user_id)) )
                    
                    print "related_users: ", related_users
                    logger.info("no. of related users: %i", len(related_users))
                    logger.debug("related users: %s", related_users)
                
                    #append all related users of each user_id in to_crawl into one big set
                    all_related_users = all_related_users.union( related_users )
            
        #print "all_related_users: ", all_related_users
        #clean up to_crawl, add all_related_users to to_crawl, except those already in snowball_set
        to_crawl = all_related_users.difference(snowball_set)
        print "to_crawl: ", len(to_crawl)

    return snowball_set

EGO = 47545000
HOPS = 4


snowball = get_snowball_s(EGO, HOPS, False)

logger.info("total crawled: %i", len(snowball))

#print snowball
print "total crawled: ", len(snowball)
print [(k, m['followers_count']) for k,m in snowball.items()]

#write to file -- raw json representation of the snowball
file = open('snowball-%d-%d.json'%(EGO,HOPS),'w')
file.write(json.dumps(snowball))




