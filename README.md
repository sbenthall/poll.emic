This is a tool for collecting data from Twitter.  Currently the focus is on egocentric networks.  After collecting and caching the data, this tool can output the data in .gexf format for visualization.

## Python Package Dependencies

* Twitter
* networkx
* simplejson
* nose

## Setup and configuration

1. Clone the repository
2. Go into the local copy

    cd poll.emic

3. Install. Currently 

    python setup.py develop

4. Add a configuration file `config.cfg` in the top level directory of your working copy.  Include the app credentials that you got from the Twitter API.  See [here](https://github.com/sbenthall/poll.emic/wiki/Sample-Configuration-File) for a sample configuration file.


## Usage

For one application of this, try running the getsnowball script.

    python bin/getsnowball.py

This should start crawling a snowball centered on a particular Twitter user.
