from poll_emic.apiwrapper import *
from poll_emic.sample import *
from pprint import pprint as pp
import unicodedata
from poll_emic.utils import call_api, dict_merge
import networkx as nx
import sys

def unu(ins):
    if type(ins) is str:
        return ins
    elif type(ins) is unicode:
        return unicodedata.normalize('NFKD', ins).encode('ascii','ignore')

def data_to_network(data):
    G = nx.DiGraph()

    for fromu in data['edges'].keys():
        for tou in data['edges'][fromu].keys():
            G.add_edge(fromu,tou,weight=data['edges'][fromu][tou])
    
    pp('Collecting lookup metadata')
    data['nodes'] = dict_merge(data['nodes'],lookup_many(G.nodes()))
    pp("Has metadata for %d users" % len(data.items()))

    for user in G.nodes():
        pp('Adding node attributes for %s' % user)

        try:
            G.node[user]['followers_count'] = data['nodes'][user]['followers_count']
            G.node[user]['friends_count'] = data['nodes'][user]['friends_count']
            G.node[user]['statuses_count'] = data['nodes'][user]['statuses_count']
            G.node[user]['depth'] = data['nodes'][user]['depth']
            G.node[user]['description'] = unu(data['nodes'][user]['description']
                                           if data['nodes'][user]['description']
                                           else 'none')
            G.node[user]['url'] = unu(data['nodes'][user]['url']
                                   if data['nodes'][user]['url']
                                   else 'none')
            G.node[user]['location'] = unu(data['nodes'][user]['location']
                                        if data['nodes'][user]['location']
                                        else 'none')
        except KeyError as e:
            print "KeyError: %s on user data:" % e
            pp(data['nodes'][user])
            pp("Removing %s" % user)
            G.remove_node(user)

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
        # proper regexes here please
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

