import os
import sys

#
# Use this script to clean out empty log files created by getLog when
# twitter bails out
#

LOG_PATH = "log/"

filenames = os.listdir(LOG_PATH)

for filename in filenames:
    path = "%s%s" % (LOG_PATH,filename)
    logfile = open(path)
    if logfile.read() == '':
        os.remove(path)
