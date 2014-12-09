import datetime
import poll_emic.cache as cache
from poll_emic.authtwitter import oauth
from pprint import pprint as pp
import sys
from twitter import TwitterStream

def main(args):

    users = []
    tags = []

    #Will cache tweets in batches
    save_rate = 100

    for arg in args:
        # to do: deal with hashtags here
        # proper regexes here please
        if arg[0] is '@':
            users.append(arg[1:])
        if arg[0] is '%':
            print "Setting save rate to %s" % (arg[1:])
            save_rate = int(arg[1:])
        else:
            tags.append(arg)

    #TODO: Convert usernames to ID numbers to make them valid 'follow' inputs

    domain = 'stream.twitter.com'

    twitter_stream = TwitterStream(auth=oauth,domain=domain)

    iterator = twitter_stream.statuses.filter(track=','.join(tags))
    
    counter = 0

    recent_tweets = []

    for tweet in iterator:
        counter = counter + 1

        pp(tweet)
        recent_tweets.append(tweet)

        if counter % save_rate == 0:
            counter = 0

            # prepare timestamp
            now = datetime.datetime.now()
            now = str(now)
            now = now.replace(' ','-')
            now = now.replace('.','-')

            query = '+'.join(tags)
            pp("Writing to %s-%s" % (query,now))

            cache.write(domain,query,recent_tweets,timestamp=now)

    #data = get_mentionball(ego,data,only_replies=True)
    #nx.write_gexf(G,"mentionball-%s.gexf" % "+".join(args).replace('/','~'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print "Please include one or more arguments."

