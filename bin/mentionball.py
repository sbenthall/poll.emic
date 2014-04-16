from poll_emic.apiwrapper import *
from poll_emic.sample import *
from pprint import pprint as pp
from poll_emic.utils import call_api
import networkx as nx
import sys


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

    egos = []

    for arg in args:
        # to do: deal with hashtags here
        if arg[0] is '@':
            if "/" in arg:
                parts = arg.split("/")
                egos.extend(get_members_from_list(parts[0][1:],parts[1]))
            else:
                egos.append(arg[1:])

    
    # replace egos with 

    data = {'nodes': {}, 'edges': {}}

    for ego in egos:
        data = get_mentionball(ego,data,only_replies=True)

    G = data_to_network(data)

    clean_ball(G)

    nx.write_gexf(G,"mentionball-%s.gexf" % "+".join(args).replace('/','~'))

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(sys.argv[1:])
    else:
        print "Please include a screen name or user ID for ego as argument."

