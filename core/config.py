import ConfigParser
import os

configurationFile = os.path.join( os.path.dirname( os.path.abspath( __file__ ) ), '../config/main.ini' )
if not os.path.exists( configurationFile ):                                      
    print 'Could not find configuration file: %s' % configurationFile
    sys.exit( 1 )
try:                                                                           
    config = ConfigParser.RawConfigParser()                                      
    config.read( configurationFile )                                             
except Exception as e:                                                           
    print 'Failed to parse config file: %s, %s' % ( configurationFile, e )
    sys.exit( 2 )     
