#!/usr/bin/env python

import argparse
import datetime
import logging
import os
import platform
import sys

currentDirectory = None


def setup_path():
    """ Set up path """
    global currentDirectory
    currentDirectory = os.path.dirname(os.path.abspath(__file__))
    for path in ['../core', '../lib', '..']:
        path = os.path.abspath(os.path.join(currentDirectory, path))
        sys.path.insert(0, path)


def setup_db():
    global currentDirectory
    # Set up database
    import core.database
    try:
        databaseFromConf = conf.get('ocarina', 'database')
    except:
        databaseFromConf = None
    if databaseFromConf is None:
        databaseFile = os.path.abspath(os.path.join(
                                       currentDirectory, '../results.db'))
    else:
        databaseFile = databaseFromConf
    db = core.database.getDatabase(databaseFile)
    return db


def main():
    setup_path()

    # Parse command line arguments
    args_parser = argparse.ArgumentParser()
    args_parser.add_argument(
        "--debug",
        help="Increase output verbosity",
        action="store_true")
    args_parser.add_argument("--tweak",
                             help="Set time and date to tweaked value")
    args_parser.add_argument("--chords",
                             help="Directory to look for scripts in")
    args_parser.add_argument( "--history",
                            help="List previous chord executions" )
    args = args_parser.parse_args()

    # Set up logging
    import core.log as log
    logging = log.getLogger(args.debug)
    logging.debug('Using Python %s', platform.python_version())

    # Load configuration
    from core.config import config as conf

    # Set up database
    db = setup_db()

    # Where are the chords kept?
    if args.chords:
        if os.path.isdir(args.chords):
            chordsDirectory = args.chords
    else:
        try:
            chordsDirectoryFromConf = conf.get('ocarina', 'chords')
            if os.path.isdir(chordsDirectoryFromConf):
                chordsDirectory = chordsDirectoryFromConf
        except:
            chordsDirectory = os.path.abspath(
                os.path.join(currentDirectory, '../chords'))
    sys.path.insert(0, chordsDirectory)

    # Where are the virtual environments kept?
    try:
        virtualEnvDirectoryFromConf = conf.get('ocarina', 'virtualenv')
        if os.path.isdir(virtualEnvDirectoryFromConf):
            virtualEnvDirectory = virtualEnvDirectoryFromConf
    except:
        virtualEnvDirectory = os.path.abspath(
            os.path.join(currentDirectory, '../.virtualenv'))

    shouldRunChords = not args.history

    if shouldRunChords:
        import core.chords as chords
        from core.now import Now
        now = Now(args.tweak)
        chords.run(chordsDirectory, virtualEnvDirectory, now, logging)

    if args.history:
        from core.history import History

        history = History( db )
        history.listPrevious( args.history )


if __name__ == "__main__":
    main()
