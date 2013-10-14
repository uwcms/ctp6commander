#!/bin/bash

export CACTUS_HOME=../cactus

export PATH=$CACTUS_HOME/trunk/cactuscore/uhal/tests/bin:$PATH
export LD_LIBRARY_PATH=$CACTUS_HOME/trunk/cactuscore/extern/boost/RPMBUILD/SOURCES/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CACTUS_HOME/trunk/cactuscore/extern/pugixml/RPMBUILD/SOURCES/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CACTUS_HOME/trunk/cactuscore/uhal/log/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CACTUS_HOME/trunk/cactuscore/uhal/grammars/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CACTUS_HOME/trunk/cactuscore/uhal/uhal/lib:$LD_LIBRARY_PATH
export LD_LIBRARY_PATH=$CACTUS_HOME/trunk/cactuscore/uhal/tests/lib:$LD_LIBRARY_PATH

export PYTHONPATH=$CACTUS_HOME/trunk/cactuscore/uhal/pycohal/pkg:$PYTHONPATH
export PYTHONPATH=$CACTUS_HOME/trunk/cactuscore/uhal/gui:$PYTHONPATH
export PYTHONPATH=$CACTUS_HOME/trunk/cactuscore/uhal/tools:$PYTHONPATH
