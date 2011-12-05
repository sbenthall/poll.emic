This repository is for tools for studying Twitter using probabilistic topic modelling.

It uses MALLET to do the topic inference, using LDA.

## Setup and usage

To execute, first unpack the mallet script:
tar -xzf mallet-2.0.6.tar-gz

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