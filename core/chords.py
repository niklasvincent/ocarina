import datetime
import importlib
import os
import sys

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

def runModule(chord, now, logging):
    try:
        module = importlib.import_module( chord )
    except Exception as e:
        logging.warn( 'Could not import %s, %s', chord, e )
    logging.debug( 'Considering whether to run %s', chord )
    try:
        shouldRun = module.shouldRun( now )
    except Exception as e:
        shouldRun = False
        logging.warn( 'Could not run shouldRun() on %s, %s', chord, e )
    logging.debug( 'shouldRun() returned %s', shouldRun )
    if shouldRun:
        try:
            logging.debug( 'Running main method on %s', chord )
            module.main()
        except Exception as e:
            logging.error( 'Failed to run %s: %s', chord, e )
            pass

def run(directory, now, logging):
    chords = findChords( directory, logging )
    for chord in chords:
        runModule( chord, now, logging )
