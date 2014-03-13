#!/usr/bin/env python

import os
import sys

# Add relevant directories to path
currentDirectory = os.path.dirname( os.path.abspath( __file__ ) )
for path in [ '../core', '../lib', '..' ]:
    path = os.path.abspath( os.path.join( currentDirectory, path ) )
    sys.path.insert( 0, path )

# Where the chords are kept
chordsDirectory = os.path.abspath( os.path.join( currentDirectory, '../chords' ) )
sys.path.insert( 0, chordsDirectory )

import core.chords as chords
from core.now import Now

chords.run( chordsDirectory, Now() )
