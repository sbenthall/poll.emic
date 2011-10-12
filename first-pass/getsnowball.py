from twitter import Twitter, TwitterHTTPError, OAuth
import ConfigParser
import urllib2
import simplejson as json
import logging
logger = logging.getLogger('getsnowball')
#todo: use date/time as the log file name
hdlr = logging.FileHandler('./logging/getsnowball.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr) 
logger.setLevel(logging.DEBUG)

THROTTLE = 1000

config= ConfigParser.ConfigParser()
config.read('config.cfg')

oauth = OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret'))

twitter = Twitter(auth=oauth)

def lookup(user_id):
    # return user's metadata information
    try:
        return twitter.users.lookup(user_id=user_id)[0]
    except TwitterHTTPError as e:
        print e
        return {'followers_count': THROTTLE+1} #hack to prevent crawling this

API_URL = "http://api.twitter.com/1/"

def get_friends(user_id):
    try:
        friends = twitter.friends.ids(user_id=user_id)
        logger.debug("id: %s \n friends: %s ", user_id, friends)
        return set(friends)
    except TwitterHTTPError as e:
        print e
        return set()

def get_followers(user_id):
    try:
        followers = friends = twitter.followers.ids(user_id=user_id)
        logger.debug("id: %s \n followers: %s ", user_id, followers)
        return set(followers)
    except TwitterHTTPError as e:
        print e
        return set()

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
        for user_id in to_crawl:
            print "user_id: ", user_id
            if user_id not in snowball_set:
                metadata = lookup(user_id)
                snowball_set[user_id] = metadata
                
                if h == hops-1:
                    pass #final hop, skip collecting freinds and followers
                    
                elif metadata['followers_count'] > THROTTLE:
                    print "followers exceed ", THROTTLE, ", skipped"
                
                else:
                    #look into each user's f&f
                    #related_users is a set of accounts that connect to user_id
                    if mutual:
                        #take intersection
                        related_users = get_friends(user_id).intersection( get_followers(user_id) )
                    else:
                        #make union
                        related_users = get_friends(user_id).union( get_followers(user_id) )
                    
                    print "related_users: ", related_users
                    logger.info("no. of related users: %i", len(related_users))
                    logger.debug("related users: %s", related_users)
                
                    #append all related users of each user_id in to_crawl into one big set
                    all_related_users = all_related_users.union( related_users )
            
        #print "all_related_users: ", all_related_users
        #clean up to_crawl, add all_related_users to to_crawl, except those already in snowball_set
        to_crawl = all_related_users.difference(snowball_set)
        print "to_crawl: ", to_crawl

    return snowball_set

EGO = 47545000
HOPS = 3


snowball = get_snowball_s(EGO, HOPS, False)

logger.info("total crawled: %i", len(snowball))

#print snowball

print [(k, m['followers_count']) for k,m in snowball.items()]

#write to file -- raw json representation of the snowball
file = open('snowball-%d-%d.json'%(EGO,HOPS),'w')
file.write(json.dumps(snowball))




