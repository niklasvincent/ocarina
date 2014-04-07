import datetime
import sys

import log
logging = log.getLogger()

class History(object):

    def __init__(self, db):
        self.db = db

    def _interpretFilter(self, filter):
        parts = filter.split( ',' )

    def listPrevious(self, filter):
        previous = self.db.getExecutions()
        rows = []
        for p in previous:
            row = [  p[0],
                    datetime.datetime.utcfromtimestamp( p[1] ),
                    p[2],
                    p[3],
                    p[4]
                    ]
            row = [ str( i ) for i in row ]
            rows.append( row )
        self.print_table( rows )

    def print_table(self, table):
        col_width = [max(len(x) for x in col) for col in zip(*table)]
        for line in table:
            print "| " + " | ".join("{:{}}".format(x, col_width[i])
                             for i, x in enumerate(line)) + " |"
