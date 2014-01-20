from poll_emic.apiwrapper import *
from collections import Counter
from itertools import chain
from pprint import pprint as pp
import networkx as nx
import sys

def get_mention_counts(user):

    pp("Getting mention counts for %s" % user)

    try:
        tweets = use_statuses_api(user)

        mentions = [tweet['entities']['user_mentions']
                    for tweet in tweets if tweet.get('retweeted_status') is None]
    
        counts = Counter([user['screen_name']
                          for user in chain.from_iterable(mentions)])
    except:
        print("Statuses response for %s was %s" % (user,tweets))

        counts = Counter()

    return counts

def get_mention_data(user,data):
    data['edges'][user] = get_mention_counts(user)


def get_mentionball(ego, data):

    get_mention_data(ego,data)

    for user in data['edges'][ego].keys():
        get_mention_data(user,data)

    return data


def data_to_network(data):
    G = nx.DiGraph()

    for fromu in data['edges'].keys():
        for tou in data['edges'][fromu].keys():
            G.add_edge(fromu,tou,weight=data['edges'][fromu][tou])
    
    pp('Collecting lookup metadata')
    data['nodes'] = lookup_many(G.nodes())
    pp("Has metadata for %d users" % len(data.items()))

    for user in G.nodes():
        pp('Adding node attributes for %s' % user)

        try:
            G.node[user]['followers_count'] = data['nodes'][user]['followers_count']
        except TwitterHTTPError as e:
            print e
            pp("Removing %s" % user)
            G.remove_node(user)
        except KeyError as e:
            pp(lookup(user))
            print e

    return G

def clean_ball(graph):
    for user in graph.nodes():
        if (len(graph.predecessors(user)) < 2 and
            len(graph.neighbors(user)) < 1):
            graph.remove_node(user)


def main(args):

    egos = [arg[1:] for arg in args if arg[0] is '@']

    data = {'nodes': {}, 'edges': {}}

    for ego in egos:
        data = get_mentionball(ego,data)

    G = data_to_network(data)

    clean_ball(G)

    nx.write_gexf(G,"mentionball-%s.gexf" % "+".join(egos))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print "Please include a screen name or user ID for ego as argument."

