import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from commons.emailtemplate import Sendemail
sender = "muthusamy.c@techvaraha.com"
password = "muthu@23_secure"


def send_email(subject, body, recipients):
    smtp_server = smtplib.SMTP_SSL('mail.techvaraha.com', 465)
    try:
        smtp_server.login(sender, password)
        msg = MIMEMultipart()
        msg.attach(MIMEText(body, "html"))
        msg['Subject'] = subject
        msg['From'] = sender
        msg['To'] = ', '.join(recipients)
        smtp_server.sendmail(sender, recipients, msg.as_string())
    except smtplib.SMTPAuthenticationError:
        print(f"Authentication Error for recipient: {recipients}")
    finally:
        smtp_server.quit()

def signup_mail_otp(mailto ):
    subject = "BSNL Employees and Citizens House Building Co-Operative Society Ltd."
    body = Sendemail()
    recipients = [mailto]
    send_email(subject, body, recipients)
