import ConfigParser
import os
import simplejson as json
from pprint import pprint as pp

# better to integrate with the method declarations.
method_names = ["twitter.users.lookup",
                "twitter.friends.ids",
                "twitter.followers.ids",
                "twitter.statuses.user_timeline"]

config= ConfigParser.ConfigParser()
config.read('config.cfg')

CACHE_PATH = config.get('Settings','cachepath')

for method_name in method_names:
    path = os.path.join(CACHE_PATH,method_name)
    if not os.path.exists(path):
        os.makedirs(path)

def file_path(method_name,user):
    return os.path.join(CACHE_PATH,method_name,"%s.json" % user)

def has(method_name,user):
    return os.path.isfile(file_path(method_name,user))

def write(method_name,user,data):
    pp("Caching result of %s for %s" % (method_name,user))
    pp(type(data))
    cache_file = open(file_path(method_name,user), 'w')
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
    
