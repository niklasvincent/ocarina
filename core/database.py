import sys
import sqlite3

from . import log
logging = log.getLogger()

from .model import model

databaseInstance = None


def getDatabase(filename='results.db'):
    global databaseInstance
    if databaseInstance is not None:
        return databaseInstance
    databaseInstance = Database(filename)
    return databaseInstance


class Database(object):

    def __init__(self, filename):
        try:
            logging.debug('Attempting to open database %s', filename)
            self.conn = sqlite3.connect(filename)
            self.cursor = self.conn.cursor()
            self._setupNecessary()
        except Exception as e:
            logging.critical('Could not open database %s: %s', filename, e)
            sys.exit(3)

    def _setupNecessary(self):
        global model
        for table in model.iterkeys():
            try:
                logging.debug('Creating table %s if necessary', table)
                self.cursor.execute(model[table])
                self.conn.commit()
            except Exception as e:
                logging.critical('Could not create table %s: %s', table, e)
                sys.exit(4)

    def recordExecution(self, start_time, chord_name, execution_time, status,
                        output):
        row = [start_time, chord_name, execution_time, status, output]
        sql = '''INSERT INTO execution VALUES( NULL, ?, ?, ?, ?, ?)'''
        try:
            self.cursor.execute(sql, row)
            self.conn.commit()
        except Exception as e:
            logging.critical(
                'Could not record execution of %s: %s', chord_name,
                e)
            sys.exit(5)

    def __del__(self):
        self.conn.close()
