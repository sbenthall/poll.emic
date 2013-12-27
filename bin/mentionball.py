from poll_emic.apiwrapper import *
from collections import Counter
from itertools import chain
from pprint import pprint as pp
import networkx as nx
import sys

def get_mention_counts(user):

    pp("Getting mention counts for %s" % user)

    tweets = use_statuses_api(user)

    mentions = [tweet['entities']['user_mentions']
                for tweet in tweets]
    
    counts = Counter([user['screen_name']
                      for user in chain.from_iterable(mentions)])

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

    for user in G.nodes():
        pp('Adding node attributes for %s' % user)

        try:
            data['nodes'][user] = lookup(user)[0] ## can we batch lookup?
            G[user]['followers_count'] = data['nodes'][user]['followers_count']
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


def main(ego):

    data = {'nodes': {}, 'edges': {}}

    data = get_mentionball(ego,data)

    G = data_to_network(data)

    clean_ball(G)

    nx.write_gexf(G,"mentionball-%s.gexf" % ego)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Please include a screen name or user ID for ego as argument."

