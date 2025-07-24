# python 3.12
# postgreSQL

import os
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

from __init__ import Logger, pkg_path

def send_email(subject, body, to_email):
    msg= EmailMessage()
    msg.set_content(body)
    msg['Subject'] = subject
    msg['From'] = 'yamini.konka@yahoo.com'
    msg['To'] = to_email
    
    dotenv_path = os.path.join(pkg_path, 'project', '.env')
    load_dotenv(dotenv_path)
    # load_dotenv()   # Load environment variables from .env file
    yahoo_password = os.getenv('YAHOO_APP_PASSWORD')  # Use environment variable for security
    try:
        with smtplib.SMTP_SSL('smtp.mail.yahoo.com', 465) as server:
            server.login(msg['From'], yahoo_password)
            server.send_message(msg)
        Logger.info(f"Email sent to {to_email}")
    except Exception as e:
        Logger.info(f"Failed to send email: {e}") 

