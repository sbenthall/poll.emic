try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': '',
    'author': 'Sebastian Benthall',
    'url': 'https://github.com/sbenthall/poll.emic',
    'download_url': 'https://github.com/sbenthall/poll.emic',
    'author_email': 'sb@ischool.berkeley.edu',
    'version': '0.1',
    'install_requires': ['nose','simplejson','twitter','networkx','numpy'],
    'packages': ['poll_emic'],
    'scripts': [],
    'name': 'poll.emic'
}

setup(**config)
