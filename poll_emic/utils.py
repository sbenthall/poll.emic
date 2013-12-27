from settings import *
import os
import simplejson as json
import time
from twitter import TwitterHTTPError
import numpy


def get_followers_count(username):
    log_name = "%s%s.json"%(LOG_PATH,username) 
    if os.path.isfile(log_name):
        log = json.loads(open(log_name,'r').read())
        return log[0]['user']['followers_count']


def call_api(method,arguments,sleep_exp=1):
    def call_again():
        s = SLEEP ** sleep_exp
        print("Sleeping for %d at %s" % (s, time.strftime('%X %x')))
        time.sleep(s)
        return call_api(method,arguments,sleep_exp + 1)

    try:
        r = method(**arguments)
        return r
    except TwitterHTTPError as e:
        print(e) 
        code = e.e.code
        # responding to error codes
        # see https://dev.twitter.com/docs/error-codes-responses
        if code == 400: # Invalid request, or rate limited
            if SLEEP ** (sleep_exp - 1) > 3600:
                # have slept for over an hour, so not rate limited
                # something is wrong with request
                raise e
            else:
                return call_again()
        elif code == 401: # Unauthorized
            raise e
        elif code == 403: # Forbidden due to update limits
            raise e
        elif code == 404: # Resource not found
            raise e
        elif code == 406: # Invalid format for search request
            raise e
        elif code == 420 or code == 429: # API rate limited
            return call_again()
        elif code == 500: # 'Something is broken'
            raise e
        elif code == 502: # Twitter is down or being upgraded
            return call_again()
        elif code == 503:
            return call_again()
        else:
            raise e



def normalize(dist):
    return (dist.T / sum(dist.T).T).T

#this is a hack
EPSILON = 0.0000000000000001

def entropy(dist):
    nd = normalize(dist) + EPSILON
    return 0 - sum((nd * numpy.log(nd)).T).T
