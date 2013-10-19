#!/usr/bin/env python

from settings import *
from poll_emic.apiwrapper import *

"""
Gets the user timeline status for everything in a snowball
"""
SNOWBALL_PATH = "snowball-14437549-2.json"

def load_snowball():
    if os.path.isfile("%s" % (SNOWBALL_PATH)):
        snowball_file = open("%s" % (SNOWBALL_PATH),'r')
        snowball = json.loads(snowball_file.read())
        return snowball
    else:
        print "error"


snowball = load_snowball()

for u_id, metadata in snowball.items():
    #print "crawling: ", line
    if metadata.has_key('screen_name'):
        screen_name = metadata['screen_name']
        
        use_statuses_api(screen_name)
    else:
        print 'No screen name for %s'%(u_id)


