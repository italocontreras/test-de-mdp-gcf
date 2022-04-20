from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
import smtplib

class Email:
  def __init__(self,e):
    self.server = smtplib.SMTP(host=os.environ['EMAIL_SMTP_HOST'],port=os.environ['EMAIL_SMTP_PORT'])
    html = f'''
      <html>
        <body>
          <p>
            Estimados,<br>
            hubo un problema en {os.environ['EMAIL_SERVICE_ID']}, por favor revisar el log. <br>
            Error: {e}.
          </p>
        </body>
      </html>
    '''
    self.html = MIMEText(html,'html')

  def connect(self):
    self.server.ehlo()
    self.server.starttls()
    self.server.login(os.environ['EMAIL_FROM'],os.environ['EMAIL_PASS'])

  def send_message(self):
    msg = MIMEMultipart('alternative')
    msg['Subject'] = os.environ['EMAIL_SUBJECT']
    msg['From'] = os.environ['EMAIL_FROM']
    msg['To'] = os.environ['EMAIL_TO']
    msg.attach(self.html)
    self.server.send_message(msg)