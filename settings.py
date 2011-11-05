
## GET SNOWBALL PARAMETERS

# User ID of the 'ego' of the snowball
EGO = 14437549

#Number of hops for snowball collection
HOPS = 3


CONNECTION_NO = 20


METADATA_PATH = "accounts/metadata/"
FRIENDS_PATH = "accounts/friends/"
FOLLOWERS_PATH = "accounts/followers/"

#when filter followers, true: pick randomly,
 #false: pick from beginning
FILTER_RANDOM = False 


## GET LOG PARAMETERS

SLEEP = 5
LOG_PATH = "log/"

SNOWBALL_PATH = "snowball-%d-%d.json" % (EGO, HOPS)


## EXTRACT PARAMETERS

DUMP_PATH = "sample-data/"
DUMP_FILE = "sample-data/tweets.txt"

JSON_LOG = True
