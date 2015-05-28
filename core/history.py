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
            row = [ identifier,
                    datetime.datetime.utcfromtimestamp( time_start ),
                    chord_name,
                    execution_time,
                    status
                    ]
            row = [ str( i ) for i in row ]
            rows.append( row )
        self.print_table( rows )

    def print_table(self, table):
        col_width = [max(len(x) for x in col) for col in zip(*table)]
        for line in table:
            print "| " + " | ".join("{:{}}".format(x, col_width[i])
                             for i, x in enumerate(line)) + " |"
