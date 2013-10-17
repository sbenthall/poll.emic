import ConfigParser
from twitter import Twitter, OAuth

config= ConfigParser.ConfigParser()
config.read('config.cfg')

oauth = OAuth(config.get('OAuth','accesstoken'),
                             config.get('OAuth','accesstokenkey'),
                             config.get('OAuth','consumerkey'),
                             config.get('OAuth','consumersecret'))

twitter = Twitter(auth=oauth)
