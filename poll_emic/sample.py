from apiwrapper import *
from collections import Counter
from itertools import chain
from pprint import pprint as pp

'''
This class contains methods and data structures for sampling
data from Twitter according to specific strategies.

It should be one layer of abstraction over the API wrapper.
'''

def get_mention_counts(user,only_replies=False):
    '''
    For a user, get a dictionary (or Counter) of who that
    user mentions in their past 200 tweets.

    Currently, don't include retweets.
    '''

    pp("Getting mention counts for %s" % user)

    try:
        tweets = use_statuses_api(user)

        mentions = [tweet['entities']['user_mentions']
                    for tweet in tweets 
                    if tweet.get('retweeted_status') is None
                    and (not only_replies
                         or tweet.get('in_reply_to_user_id') is not None)] 
    
        counts = Counter([user['screen_name']
                          for user in chain.from_iterable(mentions)])
    except:
        print("Statuses response for %s was broke" % (user))

        counts = Counter()

    return counts


def get_mentionball(ego,data,only_replies=False):

    data['edges'][ego] = get_mention_counts(ego,only_replies=only_replies)

    for user in data['edges'][ego].keys():
        if data['edges'].get(user) is None:
            data['edges'][user] = get_mention_counts(user,only_replies=only_replies)

    return data


