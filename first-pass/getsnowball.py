THROTTLE = 200

def lookup(user_id):
    # return user's metadata information
    return {'dummy': 'metadata', 'followers_count' : 4}

def get_friends(user_id):
    #return array of ids of users that user_id follows
    return [1,2,3,4,5]

def get_followers(user_id):
    #return array of ids of users that follow user_id
    return [5,6,7,8]

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

# added by sean
