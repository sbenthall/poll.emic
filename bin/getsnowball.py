from poll_emic.apiwrapper import *


def lookupMulti(user_ids):
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
            if not os.path.isfile("%s%s.json" % (METADATA_PATH, id)):
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
                    file = open('%s%s.json'%(METADATA_PATH,user['id']),'w')
                    file.write(json.dumps(user))

            except TwitterHTTPError as e:
                print e
                logger.error(e)


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




def get_snowball_s(start, hops, mutual):
    logger.info("*** snowball starts!!!")
    snowball_set = {}
    to_crawl = set({start})
    
    for h in range(hops):
        # get all friends and followers into queue
        print "hop: ", h
        all_related_users = set()
        
        # batch lookup users and cache into file
        # for performance reasons, lookupMulti mutates input
        # so copy before lookup
        lookupMulti(set(to_crawl))
        print 'after lookupMulti, to_crawl is ', to_crawl
        for user_id in to_crawl:
            #print "user_id: ", user_id
            if user_id not in snowball_set:
                # call lookup would only look at cache since lookupMulti called in advance
                metadata = lookup(user_id)
                snowball_set[user_id] = metadata
                
                if h == hops-1:
                    pass #final hop, skip collecting friends and followers
                else:
                    #look into each user's f&f
                    #related_users is a set of accounts that connect to user_id
                    if mutual:
                        #take intersection
                        related_users = filter(get_friends(user_id).intersection( get_followers(user_id)))
                    else:
                        #make union
                        related_users = filter(get_friends(user_id).union( get_followers(user_id)))
                    
                    print "related_users: ", related_users
                    logger.info("no. of related users: %i", len(related_users))
                    logger.debug("related users: %s", related_users)
                
                    #append all related users of each user_id in to_crawl into one big set
                    all_related_users = all_related_users.union( related_users )
            
        print "all_related_users: ", all_related_users
        #clean up to_crawl, add all_related_users to to_crawl, except those already in snowball_set
        to_crawl = all_related_users.difference(snowball_set)
        print "to_crawl: ", len(to_crawl)

    return snowball_set

snowball = get_snowball_s(EGO, HOPS, False)

logger.info("total crawled: %i", len(snowball))

#print snowball
print "total crawled: ", len(snowball)
print [(k, m['followers_count']) for k,m in snowball.items()]

#write to file -- raw json representation of the snowball
file = open('snowball-%d-%d.json'%(EGO,HOPS),'w')
file.write(json.dumps(snowball))



