from config import config as conf
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
import time

import pushnotify

def sendMail(recipients, subject, body):
    if not isinstance( recipients, list ):
        recipients = [ recipients ]
    session = smtplib.SMTP( conf.get( 'gmail', 'server' ), 
            conf.getint( 'gmail', 'port' ) )
    session.ehlo()
    session.starttls()
    session.login( conf.get( 'gmail', 'username' ),
            conf.get( 'gmail', 'password' ) )
    for recipient in recipients:
        headers = "\r\n".join( [ "from: " + conf.get( 'gmail', 'from' ),
            "subject: " + subject,
            "to: " + recipient,
            "mime-version: 1.0",
            "content-type: text/html" ] )
        content = headers + "\r\n\r\n" + body
        session.sendmail( conf.get( 'gmail', 'from' ), recipient, content )
    
def sendNotification(application, desc, event):
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
            conf.get( 'graphite', 'port' ) )
    sock.connect( graphite_address )
    sock.sendall( message )
    sock.close()

