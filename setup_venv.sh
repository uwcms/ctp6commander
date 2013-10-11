#!/bin/bash

# Downloads virtualenv.py, sets up an environment, and installs dependencies.
# Author: Evan K. Friis, UW

VERSION=1.10.1

curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-${VERSION}.tar.gz
tar xzf virtualenv-${VERSION}.tar.gz

python2.6 virtualenv-${VERSION}/virtualenv.py --system-site-packages env

source env/bin/activate

pip install argparse
pip install flask
pip install termcolor
