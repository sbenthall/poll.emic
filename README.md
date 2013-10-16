This is a tool for visualizing the perspective of a Twitter user's relations with others, based on publically available data.

It is a fork of `topical-topology`, an earlier research project.

## Setup and usage

settings.py has the global settings for all the scripts

then run these scripts in the following order:

getsnowball.py -> finds a 'snowball' of users
getLog.py -> logs last 200 tweets of each user in snowball
extract.py -> extracts the tweets from the logs into a format usable by MALLET
infertopics.py -> Use MALLET to infer topics on the tweets using LDA
preparedata.py -> parse data into numpy arrays and persist as .npy files

then use the analysis scripts, or write your own


## Config

To properly configure the scripts, you need to supply a file, config.cfg, with the following contents:


[OAuth]
accesstoken:realaccesstoken
accesstokenkey:realtokenkey
consumerkey:consumerkey
consumersecret:consumersecret