This is a tool for visualizing the perspective of a Twitter user's relations with others, based on publically available data.

It is a fork of `topical-topology`, an earlier research project.

## Setup and configuration

Clone the repository and run

    python setup.py develop

settings.py has the global settings

You will also need to supply a file, config.cfg, with the following information to authenticate with the TWitter API:

[OAuth]
accesstoken:realaccesstoken
accesstokenkey:realtokenkey
consumerkey:consumerkey
consumersecret:consumersecret

[Settings]
cachepath:path/to/cache/directory

## Usage

For one application of this, try running the getsnowball script.

    python bin/getsnowball.py

This should start crawling a snowball centered on a particular Twitter user.