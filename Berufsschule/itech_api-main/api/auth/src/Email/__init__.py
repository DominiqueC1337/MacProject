import smtplib
import ssl
from os import getenv
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formatdate


def send_mail(to, subject, text, files=None):
    msg = MIMEMultipart()
    msg['From'] = getenv('MAIL_FROM')
    msg['To'] = to
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject

    msg.attach(MIMEText(text))

    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)

    if getenv('MAIL_USE_SSL').lower() in ['true', '1', 'y', 'yes']:
        context = ssl.create_default_context()
        smtp = smtplib.SMTP_SSL(getenv('MAIL_SERVER'), int(getenv('MAIL_PORT')), context=context)
    else:
        smtp = smtplib.SMTP(getenv('MAIL_SERVER'), int(getenv('MAIL_PORT')))
        if getenv('MAIL_USE_TLS').lower() in ['true', '1', 'y', 'yes']:
            smtp.starttls()

    smtp.login(getenv('MAIL_USERNAME'), getenv('MAIL_PASSWORD'))
    smtp.sendmail(getenv('MAIL_FROM'), to, msg.as_string())
    smtp.close()
