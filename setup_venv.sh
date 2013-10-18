#!/bin/bash

# Downloads virtualenv.py, sets up an environment, and installs dependencies.
# ONLY needed for unfinished 
# Author: Evan K. Friis, UW

VERSION=1.10.1

curl -O https://pypi.python.org/packages/source/v/virtualenv/virtualenv-${VERSION}.tar.gz
tar xzf virtualenv-${VERSION}.tar.gz

python2.6 virtualenv-${VERSION}/virtualenv.py --system-site-packages env

THIS_DIR=`pwd`
echo "export CTP6_CONNECTION=$THIS_DIR/ctp6_connections.xml" >> env/bin/activate
source env/bin/activate

pip install flask
