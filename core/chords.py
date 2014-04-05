import datetime
import importlib
import os
import sys
import time

from capturing import Capturing
from status import Status

import database
db = database.getDatabase()

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
    error = None
    with Capturing() as output:
        try:
            function()
        except Exception as e:
            error = e
    # Convert to milliseconds
    elapsed = ( timer() - t0 ) * 1000
    return ( elapsed, output, error )

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
        start_time = int( time.time() )
        status = Status.FAIL
        logging.debug( 'Running main method on %s', chord )
        executionTime, output, error = execute( module.main )
        logging.debug( 'Ran main method on %s in %f ms', chord, executionTime )
        if error is None:
            status = Status.SUCCESS
        else:
            logging.error( 'Failed to run %s: %s', chord, error )
            output = "%s\n%s" % ( output, error )
        db.recordExecution( start_time, chord, executionTime, 
                status, str( output ) )

def run(directory, now, logging):
    chords = findChords( directory, logging )
    for chord in chords:
        runModule( chord, now, logging )
