CTP6 Commander
==============

This package includes a command-line and web interface for controlling the
optical transceivers on the CTP6.

Installation
============

This package depends on a local installation of the microHAL.

Installing microHAL
-------------------

From [CACTUS][https://svnweb.cern.ch/trac/cactus/wiki/DevInstructions]. Follow
the instructions at:

https://svnweb.cern.ch/trac/cactus/wiki/uhalQuickTutorial#HowtoInstalltheIPbusSuite

to install via yum.  Requires ROOT. Then ``source environment.sh`` to get
things setup.


Building the virtualenv for the (unfinished) web interface
----------------------------------------------------------

Executing ``./setup_venv.sh`` will create a python virtualenv with the
necessary dependencies.  You'll need to ``source env/bin/activate`` every time
you start a new session.
