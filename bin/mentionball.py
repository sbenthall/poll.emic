from poll_emic.apiwrapper import *
from collections import Counter
from itertools import chain
from pprint import pprint as pp

USER = 'sbenthall'

DATA = {}

def get_mention_counts(user):
    mentions = [tweet['entities']['user_mentions'] for tweet in use_statuses_api(user)]
    
    counts = Counter([user['screen_name'] for user in chain.from_iterable(mentions)])

    return counts


DATA[USER] = get_mention_counts(USER)

for user in DATA[USER].keys():
    DATA[user] = get_mention_counts(user)

pp(DATA)

file = open('mentionball.json','w')
file.write(json.dumps(DATA))
