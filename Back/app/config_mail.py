import os

sender_mail=os.environ.get('SENDER_EMAIL')  

app_password=os.environ.get('APP_PASSWORD') 

class Config:
    MAIL_SERVER = 'smtp.googlemail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = sender_mail
    MAIL_PASSWORD =app_password
    
    MAIL_DEBUG = True
    MAIL_SUPPRESS_SEND = False

    MAIL_DEFAULT_SENDER = (' Mail Notification Application Dashboard De Compte AWS ','noreply@gmail.com')
    MAIL_MAX_EMAILS = None
    MAIL_ASCII_ATTACHMENTS = False
