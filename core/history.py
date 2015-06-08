import datetime
import sys

import log
logging = log.getLogger()

class History(object):

    def __init__(self, db):
        self.db = db

    def _interpretFilter(self, filter):
        parts = filter.split( ',' )

    def listPrevious(self, chord_name):
        previous = self.db.getExecutions( chord_name = chord_name )
        rows = []
        for p in previous:
            identifier, time_start, chord_name, execution_time, status, output = p
            status = "OK" if status else "FAILED"
            row = [ identifier,
                    datetime.datetime.utcfromtimestamp( time_start ),
                    chord_name,
                    execution_time,
                    status,
                    ]
            row = [ str( i ) for i in row ]
            row = "| ".join(row)
            print "-" * len(row)
            print row
            print output

