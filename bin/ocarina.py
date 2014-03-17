#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import platform
import sys

# Parse command line arguments 
args_parser = argparse.ArgumentParser()
args_parser.add_argument( "--debug", help="Increase output verbosity", action="store_true" )
args_parser.add_argument( "--tweak", help="Set time and date to tweaked value" )
args_parser.add_argument( "--chords", help="Directory to look for scripts in" )
args = args_parser.parse_args()

# Add relevant directories to path
currentDirectory = os.path.dirname( os.path.abspath( __file__ ) )
for path in [ '../core', '../lib', '..' ]:
    path = os.path.abspath( os.path.join( currentDirectory, path ) )
    sys.path.insert( 0, path )

# Load configuration
from core.config import config as conf

# Set up logging
import core.log as log
logging = log.getLogger( args.debug )

logging.debug( 'Using Python %s', platform.python_version() )

# Where are the chords kept?
if args.chords:
    if os.path.isdir( args.chords ):
        chordsDirectory = args.chords
else:
    try:
        chordsDirectoryFromConf = conf.get( 'ocarina', 'chords' )
        if os.path.isdir( chordsDirectoryFromConf ):
            chordsDirectory = chordsDirectoryFromConf
    except:
        chordsDirectory = os.path.abspath( os.path.join( currentDirectory, '../chords' ) )
sys.path.insert( 0, chordsDirectory )

import core.chords as chords
from core.now import Now

now = Now( args.tweak )
chords.run( chordsDirectory, now, logging )
