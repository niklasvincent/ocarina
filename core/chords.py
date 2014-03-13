import datetime
import importlib
import os

def findChords(directory, logging):
    chords = []
    logging.debug( 'Looking for chords in %s', directory )
    for root, dirs, files in os.walk( directory ):
        files = [ f for f in files if not f.endswith( '.pyc' ) ]
        files = [ f for f in files if f.endswith( '.py' ) ]
        for file in files:
            package = os.path.basename( root )
            name = file.split( '.' )[0]
            module = "%s.%s" % ( package, name )
            if name != '__init__':
                logging.debug( 'Found chord %s', file )
                chords.append( module )
    return chords

def runModule(chord, now, logging):
    module = importlib.import_module( chord )
    logging.debug( 'Considering whether to run %s', chord )
    shouldRun = module.shouldRun( now )
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
