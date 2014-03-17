import logging
import sys

loggingInstance = None

def getLogger(debug=False):
    global loggingInstance
    if loggingInstance is not None:
        return loggingInstance
    root = logging.getLogger()
    ch = logging.StreamHandler( sys.stdout )
    formatter = logging.Formatter( '%(asctime)s - ocarina - %(levelname)s - %(message)s' )
    ch.setFormatter( formatter )
    root.addHandler( ch )
    if debug:
        ch.setLevel( logging.DEBUG )
        root.setLevel( logging.DEBUG )
    else:
        ch.setLevel( logging.INFO )
        root.setLevel( logging.INFO )
    loggingInstance = logging
    return loggingInstance
