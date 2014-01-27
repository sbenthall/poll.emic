from nose.tools import *
from poll_emic.apiwrapper import *
import poll_emic.cache as cache
import logging
import itertools

test_user = 'twitter'
test_users = [test_user,'sbenthall']
test_list = 'engineering'

def setup():
    for method in cache.method_names:
        cache.clear(method,test_users)
    print "SETUP!"

def teardown():
    print "TEAR DOWN!"

@with_setup(setup,teardown)
def lookup_test():
    data = lookup(test_user)
    assert isinstance(data,dict), 'output is not a dict'
    assert data['screen_name'] == 'twitter', 'mismatched screen_name'

@with_setup(setup,teardown)
def get_friends_test():
    data = get_friends(test_user)
    assert isinstance(data,set), 'output is not a set'

@with_setup(setup,teardown)
def get_followers_test():
    data = get_followers(test_user)
    assert isinstance(data,set), 'output is not a set'

@with_setup(setup,teardown)
def use_statuses_api_test():
    data = use_statuses_api(test_user)
    assert isinstance(data,list), 'output is not a list'
    logger.debug("Length of statuses data is %d" % len(data))
    assert len(data) == 200, 'output does not have 200 tweets' 

@with_setup(setup,teardown)
def lookup_many_test():
    data = lookup_many(test_users)

    assert isinstance(data,dict), 'lookup_many data is not a dict'
    assert len(data.items()) == 2, 'lookup_many did not return 2 profiles'

    cache.clear('twitter.users.lookup',test_user)
    data = lookup_many(itertools.repeat(test_user,110))

@with_setup(setup,teardown)
def get_members_from_list(owner,slug):
    members = get_members_from_list(test_user,test_list)
    assert isinstance(members,list)
    assert isinstance(members[0],string)
