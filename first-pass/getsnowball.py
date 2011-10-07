from twitter import Twitter, TwitterHTTPError, OAuth
import ConfigParser
import urllib2
import simplejson as json

THROTTLE = 1000

config= ConfigParser.ConfigParser()
config.read('config.cfg')

twitter = Twitter(auth=OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret')))

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
        url = "%sfriends/ids.json?user_id=%d" % (API_URL, user_id)
        from_twitter = urllib2.urlopen(url)
        friends = json.loads(from_twitter.read())
        return set(friends)
    except urllib2.HTTPError:
        return set()


    return {755994494} #twitter.friends(user_id=user_id)

def get_followers(user_id):
    try:
        url = "%sfollowers/ids.json?user_id=%d" % (API_URL, user_id)
        from_twitter = urllib2.urlopen(url)
        followers = json.loads(from_twitter.read())
        return set(followers)
    except urllib2.HTTPError:
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
                
                    #append all related users of each user_id in to_crawl into one big set
                    all_related_users = all_related_users.union( related_users )
            
        #print "all_related_users: ", all_related_users
        #clean up to_crawl, add all_related_users to to_crawl, except those already in snowball_set
        to_crawl = all_related_users.difference(snowball_set)
        print "to_crawl: ", to_crawl

    return snowball_set


snowball = get_snowball_s(47545000, 2, False)

print snowball

print [(k, m['followers_count']) for k,m in snowball.items()]







