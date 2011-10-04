from twitter import Twitter, TwitterHTTPError, OAuth
import ConfigParser

THROTTLE = 2000

config= ConfigParser.ConfigParser()
config.read('config.cfg')

twitter = Twitter(auth=OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret')))

def lookup(user_id):
    # return user's metadata information
    return {'screen_name': 'abc', 'followers_count' : 4}

def get_friends(user_id):
    #return array of ids of users that user_id follows
    return {1,2,3,4,5}

def get_followers(user_id):
    #return array of ids of users that follow user_id
    return {5,6,7,8}

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
                
                if metadata['followers_count'] < THROTTLE:
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
                
                else:
                    print "followers exceed ", THROTTLE, ", skipped"
            
        #print "all_related_users: ", all_related_users
        #clean up to_crawl, add all_related_users to to_crawl, except those already in snowball_set
        to_crawl = all_related_users.difference(snowball_set)
        print "to_crawl: ", to_crawl

    return snowball_set

print get_snowball_s(4, 2, False)






