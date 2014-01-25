import calendar
import os
import simplejson as json
import time
from twitter import TwitterHTTPError
import numpy

def call_api(method,arguments):
    def call_again():
        print "The big sleep"
        time.sleep(2600)
        return call_api(method,arguments)

    try:
        r = method(**arguments)

        print "Rate limit remaining: %d" % r.rate_limit_remaining

        if r.rate_limit_remaining < 1:
            sleep_time = r.rate_limit_reset - \
                calendar.timegm(time.gmtime())

            reset_time = time.strftime("%H:%M:%S",
                                       time.localtime(r.rate_limit_reset))

            print "Sleeping until %s" % reset_time

            time.sleep(sleep_time)
            
        return r
    except TwitterHTTPError as e:
        print(e) 
        code = e.e.code
        # responding to error codes
        # see https://dev.twitter.com/docs/error-codes-responses
        if code == 400: # Invalid request, or rate limited
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
