import os
from pysendpulse.pysendpulse import PySendPulse

def sp_send_simple_email(subject, html, text, to_name, to_email):
    EMAIL_REST_API_ID = os.environ['EMAIL_REST_API_ID']
    EMAIL_REST_API_SECRET = os.environ['EMAIL_REST_API_SECRET']
    EMAIL_TOKEN_STORAGE = os.environ['EMAIL_TOKEN_STORAGE']
    EMAIL_SENDER_NAME = os.environ['EMAIL_SENDER_NAME']
    EMAIL_SENDER_ID = os.environ['EMAIL_SENDER_ID']

    SPApiProxy = PySendPulse(EMAIL_REST_API_ID, EMAIL_REST_API_SECRET, EMAIL_TOKEN_STORAGE)
    email = {
        'subject': subject,
        'html': html,
        'text': text,
        'from': { 'name': EMAIL_SENDER_NAME, 'email': EMAIL_SENDER_ID },
        'to': [
            { 'name': to_name, 'email': to_email }
        ]
    }
    
    SPApiProxy.smtp_send_mail(email)