import os

NAME_PATH = "names.txt"
LOG_PATH = "log/"

def get_name():

    if os.path.isfile("%s" % (NAME_PATH)):
        names = open("%s" % (NAME_PATH),'r')
        return names
    else:
        print "error"


if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)
names = get_name()

for line in names:
    #print "crawling: ", line
	cmd = "twitter-log " + line.strip() + " > " + LOG_PATH + line.strip() + ".txt"
	print cmd
	os.system(cmd)