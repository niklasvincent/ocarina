import datetime
import importlib
import os
import sys
import time

from core.capturing import Capturing

def findChords(directory, logging):
    chords = []
    logging.debug( 'Looking for chords in %s', directory )
    for root, dirs, files in os.walk( directory ):
        files = [ f for f in files if not f.endswith( '.pyc' ) ]
        files = [ f for f in files if f.endswith( '.py' ) ]
        for file in files:
            logging.debug( 'Adding %s to path', root )
            sys.path.insert( 0, root )
            name = file.split( '.' )[0]
            if name != '__init__':
                logging.debug( 'Found chord %s', file )
                chords.append( name )
    return chords

def execute(function):
    if sys.platform == 'win32':
        timer = time.clock
    else:
        timer = time.time
    t0 = timer()
    with Capturing() as output:
        function()
    # Convert to milliseconds
    elapsed = ( timer() - t0 ) * 1000
    return ( elapsed, output )

def runModule(chord, now, logging):
    try:
        module = importlib.import_module( chord )
    except Exception as e:
        logging.warn( 'Could not import %s, %s', chord, e )
        return
    logging.debug( 'Considering whether to run %s', chord )
    if hasattr( module, 'shouldRun' ):
        try:
            shouldRun = module.shouldRun( now )
        except Exception as e:
            shouldRun = False
            logging.warn( 'Could not run shouldRun() on %s, %s', chord, e )
        logging.debug( 'shouldRun() returned %s', shouldRun )
    else:
        logging.debug( 'No shouldRun() found on %s, assuming it should run always',
                chord )
        shouldRun = True
    if shouldRun:
        try:
            logging.debug( 'Running main method on %s', chord )
            executionTime, output = execute( module.main )
            logging.debug( 'Ran main method on %s in %f ms', chord, executionTime )
        except Exception as e:
            logging.error( 'Failed to run %s: %s', chord, e )
            pass

def run(directory, now, logging):
    chords = findChords( directory, logging )
    for chord in chords:
        runModule( chord, now, logging )
