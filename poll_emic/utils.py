import calendar
import os
import simplejson as json
import time
from twitter import TwitterHTTPError
from copy import deepcopy

def call_api(method,arguments):
    def call_again():
        print "Error received. Did not catch properly. Sleeping 17 minutes"
        time.sleep(1020)
        return call_api(method,arguments)

    try:
        r = method(**arguments)

        print "Rate limit remaining: %d" % r.rate_limit_remaining

        if r.rate_limit_remaining < 1:
            sleep_time = 60 + r.rate_limit_reset - \
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
            ## It would be better to cache these results
            ## as unauthorized--this status does not change
            ## frequently and 
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

