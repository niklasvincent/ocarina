import datetime
import hashlib
import importlib
import os
import sys
import time

from collections import namedtuple

from capturing import Capturing
from status import Status
from virtualenvironment import IsolatedVirtualEnvironment

import database
db = database.getInstance()

Chord = namedtuple('Chord', ['path', 'name'])

def findChords(directory, logging):
    chords = []
    logging.debug('Looking for chords in %s', directory)
    for path, dirs, files in os.walk(directory):
        files = [f for f in files if not f.endswith('.pyc')]
        files = [f for f in files if f.endswith('.py')]
        for file in files:
            name = file.split('.')[0]
            if name != '__init__':
                logging.debug('Found chord %s', file)
                chords.append(Chord(path, name))
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
    elapsed = (timer() - t0) * 1000
    return (elapsed, output, error)

def shouldRun(module, now, logging):
    run = False
    if hasattr(module, 'shouldRun'):
         try:
              run = module.shouldRun(now)
         except Exception as e:
             logging.warn('Could not run shouldRun() on %s, %s', module.__name__, e)
         logging.debug('shouldRun() returned %s', run)
    else:
         logging.debug(
             'No shouldRun() found on %s, assuming it is a library',
             module.__name__)
         run = False 
    return run

def requiresVirtualEnv(module):
    return hasattr(module, 'requirements') and isinstance(module.requirements, (list, tuple))

def virtualEnvSignature(requirements):
    hasher = hashlib.sha1()
    hasher.update(",".join(sorted(set(requirements))))
    return hasher.hexdigest()

def virtualEnvForModule(module, virtualEnvDirectory, logging):
    logging.debug('Checking if %s needs to run in a virtualenv', module.__name__)
    virtualEnv = None
    if requiresVirtualEnv(module):
        logging.debug('%s requires virtualenv', module.__name__)
        virtualEnv = os.path.join(virtualEnvDirectory, virtualEnvSignature(module.requirements))
    logging.debug('virtualenv for %s is %s', module.__name__, virtualEnv)
    return virtualEnv

def runModule(chord, virtualEnvDirectory, now, logging):
    logging.debug("-" * 60)
    try:
        logging.debug('Adding %s to path', chord.path)
        sys.path.insert(0, chord.path)
        module = importlib.import_module(chord.name)
    except Exception as e:
        logging.warn('Could not import %s: %s', chord.name, e)
        return
    logging.debug('Considering whether to run %s', chord.name)
    if shouldRun(module, now, logging):
        virtualEnv = virtualEnvForModule(module, virtualEnvDirectory, logging)
        start_time = int(time.time())
        status = Status.FAIL
        logging.debug('Running main method on %s', chord.name)
        with IsolatedVirtualEnvironment(module, virtualEnv, logging):
            executionTime, output, error = execute(module.main)
        logging.debug('Ran main method on %s in %f ms', chord.name, executionTime)
        if error is None:
            status = Status.SUCCESS
        else:
            logging.error('Failed to run %s: %s', chord.name, error)
            output = "%s\n%s" % (output, error)
        logging.debug('Removing %s from path', sys.path[0])
        del sys.path[0]
        db.recordExecution(start_time, chord.name, executionTime,
                           status, str(output))


def run(directory, virtualEnvDirectory, now, logging):
    chords = findChords(directory, logging)
    for chord in chords:
        runModule(chord, virtualEnvDirectory, now, logging)
