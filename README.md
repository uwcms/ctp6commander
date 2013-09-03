CTP6 Commander
==============

This package includes a command-line and web interface for controlling the
optical transceivers on the CTP6.

Installation
============

This package depends on a local installation of the microHAL, as well as a
custom python environment.

Sane version of python
----------------------

```shell
source /cvmfs/cms.hep.wisc.edu/osg/app/cmssoft/cms/slc5_amd64_gcc462/external/python/2.7.3-cms4/etc/profile.d/init.sh
```

Installing microHAL
-------------------

From [CACTUS][https://svnweb.cern.ch/trac/cactus/wiki/DevInstructions].

This checks out more than a gig of junk, so you may want to install it on the
scratch disk.
```shell
svn co svn+ssh://svn.cern.ch/reps/cactus/trunk cactus/trunk --depth immediates
svn update --set-depth infinity \
        cactus/trunk/cactuscore/uhal \
        cactus/trunk/cactuscore/extern \
        cactus/trunk/config

cd cactus/trunk
make Set=uhal
```
then run 
```shell
source setup_uhal.sh
```
to setup the necessary environment.


Building the virtualenv
-----------------------

Executing ``./setup_venv.sh`` will create a python virtualenv with the
necessary dependencies.  You'll need to ``source env/bin/activate`` every time
you start a new session.
