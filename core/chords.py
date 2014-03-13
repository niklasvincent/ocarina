import datetime
import importlib
import os

def today():
    now = datetime.datetime.today().timetuple()
    print now

def findChords(directory, now):
    for root, dirs, files in os.walk( directory ):
        files = [ f for f in files if f.endswith( '.pyc' ) ]
        for file in files:
            package = os.path.basename( root )
            name = file.split( '.' )[0]
            module = "%s.%s" % ( package, name )
            if name != '__init__':
                print module
                chord = importlib.import_module( module )
                shouldRun = chord.shouldRun( now )
                print shouldRun
                if shouldRun:
                    try:
                        chord.main()
                    except:
                        pass


def run(directory, now):
    findChords( directory, now )
