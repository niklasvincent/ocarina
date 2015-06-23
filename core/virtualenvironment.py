import os
import sys

virtualEnvManagerAvailable = False
try:
    from virtualenvapi.manage import VirtualEnvironment
    virtualEnvManagerAvailable = True
except:
    pass

class IsolatedVirtualEnvironment(object):

    environmentDirectory = None
    logging = None

    prevOsPath = None
    prevSysPath = None

    def __init__(self, module, environmentDirectory, logging):
        self.environmentDirectory = environmentDirectory
        self.logging = logging
        if not environmentDirectory:
            logging.debug('No virtual environment will be set up for %s', module.__name__)
            return
        if not virtualEnvManagerAvailable:
            logging.error(
                '%s requires virtualenv, but virtualenvapi is not installed!',
                module.__name__
            )
            sys.exit(10)
        if not os.path.exists(environmentDirectory):
            try:
                os.makedirs(environmentDirectory)
            except Exception as e:
                logging.error('Could not create virtualenv directory %s: %s', environmentDirectory, e)
        venv = VirtualEnvironment(environmentDirectory)
        for requirement in set(module.requirements):
            logging.debug(
                'Checking if %s is already installed in %s',
                requirement,
                environmentDirectory
            )
            try:
                if not venv.is_installed(requirement):
                    logging.debug('%s not installed in %s', requirement, environmentDirectory)
                    venv.install(requirement)
                    logging.debug('%s installed in %s', requirement, environmentDirectory)
                else:
                    logging.debug('%s already in %s', requirement, environmentDirectory)
            except Exception as e:
                logging.error('Could not install dependency %s in %s: %s', requirement, environmentDirectory, e)

    def __enter__(self, *args):
        self.prevOsPath = os.environ['PATH']
        self.prevSysPath = list(sys.path)
        activate_this_file = os.path.join(self.environmentDirectory, "bin/activate_this.py")
        self.logging.debug(
            'Activating virtualenv %s using %s',
            self.environmentDirectory,
            activate_this_file
        )
        self.logging.debug('Previous PYTHONPATH contains %d entries', len(sys.path))
        execfile(activate_this_file, dict(__file__ = activate_this_file))
        self.logging.debug('New PYTHONPATH contains %d entries', len(sys.path))

    def __exit__(self, *args):
        self.logging.debug('Deactivating virtualenv %s', self.environmentDirectory)
        os.environ['PATH'] = self.prevOsPath
        for potentialNewItem in list(sys.path):
            sys.path.remove(potentialNewItem)
        for previousItem in list(self.prevSysPath):
            sys.path.append(previousItem)
        self.logging.debug('Restored PYTHONPATH contains %d entries', len(sys.path))


