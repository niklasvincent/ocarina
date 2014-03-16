#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import platform
import sys

root = logging.getLogger()
ch = logging.StreamHandler( sys.stdout )
formatter = logging.Formatter( '%(asctime)s - ocarina - %(levelname)s - %(message)s' )
ch.setFormatter( formatter )
root.addHandler( ch )

# Parse command line arguments 
args_parser = argparse.ArgumentParser()
args_parser.add_argument( "--debug", help="Increase output verbosity", action="store_true" )
args_parser.add_argument( "--tweak", help="Set time and date to tweaked value" )
args_parser.add_argument( "--chords", help="Directory to look for scripts in" )
args = args_parser.parse_args()

 # Adjust logging to desired verbosity
if args.debug:
  ch.setLevel( logging.DEBUG )
  root.setLevel( logging.DEBUG ) 
else:
  ch.setLevel( logging.INFO )
  root.setLevel( logging.INFO )

logging.debug( 'Using Python %s', platform.python_version() )

# Add relevant directories to path
currentDirectory = os.path.dirname( os.path.abspath( __file__ ) )
for path in [ '../core', '../lib', '..' ]:
    path = os.path.abspath( os.path.join( currentDirectory, path ) )
    sys.path.insert( 0, path )

# Load configuration
from core.config import config as conf

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
