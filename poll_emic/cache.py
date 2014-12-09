import ConfigParser
import os
import simplejson as json
from pprint import pprint as pp

# better to integrate with the method declarations.
method_names = ["twitter.users.lookup",
                "twitter.friends.ids",
                "twitter.followers.ids",
                "twitter.statuses.user_timeline",
                "stream.twitter.com"]

config= ConfigParser.ConfigParser()
config.read('config.cfg')

CACHE_PATH = config.get('Settings','cachepath')

def setup_dir(method_name):
    path = os.path.join(CACHE_PATH,method_name)
    if not os.path.exists(path):
        os.makedirs(path)

for method_name in method_names:
    setup_dir(method_name)
    #path = os.path.join(CACHE_PATH,method_name)
    #if not os.path.exists(path):
    #    os.makedirs(path)


def file_path(method_name,query,timestamp=None):
    if timestamp is not None:
        query = "%s-%s" % (query,timestamp)
    return os.path.join(CACHE_PATH,method_name,"%s.json" % query)

def has(method_name,user):
    return os.path.isfile(file_path(method_name,user))

def write(method_name,query,data,timestamp=None):
    pp("Caching result of %s for %s" % (method_name,query))
    pp(type(data))
    path = file_path(method_name,query,timestamp=timestamp)
    cache_file = open(path, 'w')
    cache_file.write(json.dumps(data))

def clear(method_name,users):
    ## TO DO: option to clear whole cache
    users = [users] if type(users) is not list else users

    for user in users:
        if has(method_name,user):
            os.remove(file_path(method_name,user))

def read(method_name,user):
        file = open(file_path(method_name,user))
        return json.loads(file.read())
    
