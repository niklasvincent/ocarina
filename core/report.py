from config import config as conf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import socket
import time
import warnings

# This is an optional dependency
try:
    import pushnotify
    pushnotifyAvailable = True
except ImportError as e:
    pushnotifyAvailable = False
    pass

def sendMail(recipients, subject, body):
    if not isinstance( recipients, list ):
        recipients = [ recipients ]
    session = smtplib.SMTP( conf.get( 'email', 'server' ), 
            conf.getint( 'email', 'port' ) )
    session.ehlo()
    session.starttls()
    session.login( conf.get( 'email', 'username' ),
            conf.get( 'email', 'password' ) )
    for recipient in recipients:
        headers = "\r\n".join( [ "from: " + conf.get( 'email', 'from' ),
            "subject: " + subject,
            "to: " + recipient,
            "mime-version: 1.0",
            "content-type: text/html" ] )
        content = headers + "\r\n\r\n" + body
        session.sendmail( conf.get( 'email', 'from' ), recipient, content )

def sendNotification(application, desc, event):
    if not pushnotifyAvailable:
        warnings.warn( 'Pushnotify is required for sending push notifications' )
        return
    client = pushnotify.get_client('nma', application=application )
    client.add_key( conf.get( 'notifymyandroid', 'api_key' ) )
    try:
        client.notify( desc, event, split=True )
    except:
        pass

def sendToGraphite(path, value):
    message = '%s %s %d\n' % ( path, value, int( time.time() ) )
    sock = socket.socket()
    graphite_address = ( conf.get( 'graphite', 'server' ), 
            int( conf.get( 'graphite', 'port' ) ) )
    sock.connect( graphite_address )
    sock.sendall( message )
    sock.close()

