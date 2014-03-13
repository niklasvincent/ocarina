#!/usr/bin/env python

import argparse
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

# Where the chords are kept
chordsDirectory = os.path.abspath( os.path.join( currentDirectory, '../chords' ) )
sys.path.insert( 0, chordsDirectory )

import core.chords as chords
from core.now import Now

chords.run( chordsDirectory, Now(), logging )
