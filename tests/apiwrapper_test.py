from nose.tools import *
from poll_emic.apiwrapper import *

def setup():
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

@with_setup(setup,teardown)
def lookup_test():
    data = lookup('twitter')
    assert isinstance(data,list), 'output is not a list'
    assert data[0]['screen_name'] == 'twitter', 'mismatched screen_name'

@with_setup(setup,teardown)
def get_friends_test():
    data = get_friends('twitter')
    assert isinstance(data,set), 'output is not a set'

@with_setup(setup,teardown)
def get_followers_test():
    data = get_followers('twitter')
    assert isinstance(data,set), 'output is not a set'
