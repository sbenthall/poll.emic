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

def get_mention_data(ego):
    data = {}

    data[ego] = get_mention_counts(ego)

    for user in data[ego].keys():
        data[user] = get_mention_counts(user)

    pp(data)

    return data

def data_to_network(data):
    G = nx.DiGraph()

    for fromu in data.keys():
        for tou in data[fromu].keys():
            G.add_edge(fromu,tou,weight=data[fromu][tou])

    return G

def clean_ball(graph):
    for user in graph.nodes():
        if (len(graph.predecessors(user)) < 2 and
            len(graph.neighbors(user)) < 1):
            graph.remove_node(user)


def main(ego):

    data = get_mention_data(ego)

    G = data_to_network(data)

    clean_ball(G)

    nx.write_gexf(G,"mentionball-%s.gexf" % ego)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print "Please include a screen name or user ID for ego as argument."

