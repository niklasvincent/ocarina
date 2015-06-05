import logging

class MockLoggingHandler(logging.Handler):
    """Mock logging handler to check for expected logs.

    Messages are available from an instance's ``messages`` dict, in order, indexed by
    a lowercase log level string (e.g., 'debug', 'info', etc.).
    """

    def __init__(self, *args, **kwargs):
        self.messages = {'debug': [], 'info': [], 'warning': [], 'error': [],
                         'critical': []}
        super(MockLoggingHandler, self).__init__(*args, **kwargs)

    def emit(self, record):
        "Store a message from ``record`` in the instance's ``messages`` dict."
        self.acquire()
        try:
            self.messages[record.levelname.lower()].append(record.getMessage())
        finally:
            self.release()

    def reset(self):
        self.acquire()
        try:
            for message_list in self.messages.values():
                message_list.clear()
        finally:
            self.release()

def getLogger():
    logger = logging.getLogger()
    handler = MockLoggingHandler(level='DEBUG')
    logger.addHandler(handler)
    return logger

def createModule(name, source):
    import types
    import sys
    module = types.ModuleType( name, source )
    module.__file__ = name + '.pyc'
    sys.modules[name] = module
    byte_code = compile( source, name, 'exec' )
    exec byte_code in module.__dict__
    return module